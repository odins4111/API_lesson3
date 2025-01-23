import requests
import json
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
import csv
import argparse
import logging
import sys
from tqdm import tqdm
import time

# Настройка логирования в начале файла
logging.basicConfig(
    filename='migration.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8'
)


def dict_to_list(value):
    if pd.isna(value) or value is None:
        return None
    return str(value).split(';')


def state_story_transform(state):
    state_mapping = {
        "new": "new",
        "reopened": "reopened",
        "active": "inProgress",
        "resolved": "resultAcceptance",
        "analysis done": "analysisdonee",
        "closed": "closed",
        "on hold": "onHold",
        "test failed": "testfailed",
        "test passed": "testpassed",
        "testing": "testing"
    }
    return state_mapping.get(state.lower(), state.lower())


def priority_story_transform(priority):
    priority_mapping = {
        "1": "minor",
        "2": "normal",
        "3": "critical",
    }
    priority = priority.lower()
    return priority_mapping.get(priority, priority)


def bug_description(attributes):
    sections = {
        'precondition': 'Precondition',
        'actual_result': 'Actual Result',
        'repro_steps': 'Repro Steps',
        'expected_result_description': 'Expected Result Description'
    }

    description_parts = []
    for key, header in sections.items():
        if not pd.isna(attributes.get(key)):
            description_parts.extend([f"<h2>{header}</h2>", attributes[key]])

    return ' '.join(description_parts)


def migration(token, org_id, attributes, title, type):
    url = "https://api.tracker.yandex.net/v2/issues/_import"
    headers = {
        "Authorization": token,
        "X-Org-ID": org_id,
        "Content-Type": "application/json"
    }

    description = bug_description(attributes) if type == "bug" else str(attributes.get('description'))

    data = {
        "queue": "PS",
        "summary": title,
        "createdAt": time_transform(attributes.get('created_date')),
        "createdBy": "8000000000000004",
        "type": type,
        "azureId": attributes.get('id'),
        "description": description,
        "assignee": "8000000000000004",
        "status": state_story_transform(attributes.get('state')),
        "affectsprojects": dict_to_list(attributes.get('projects')),
        "mustbefixedin": dict_to_list(attributes.get('fix_version')),
        "priority": priority_story_transform(str(attributes.get('priority'))),
        "components": dict_to_list(attributes.get('components')),
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        logging.info(
            "Задача создана | Тип: %s | Azure ID: %s | Yandex ID: %s",
            type,
            attributes.get('id'),
            response.json()['key']
        )

        if not pd.isna(attributes.get('parent')):
            logging.debug(
                "Найден родительский элемент | Тип: %s | ID: %s",
                type,
                attributes.get('parent')
            )
            find_task(token, org_id, attributes.get('parent'), response.json()['key'], type)

    except requests.exceptions.RequestException as e:
        logging.error(
            "Ошибка миграции | Тип: %s | Azure ID: %s | Ошибка: %s",
            type,
            attributes.get('id'),
            str(e),
            exc_info=True
        )


def log(message):
    with open('LogMigrationYandex.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message])


def time_transform(input_time):
    timestamp = pd.Timestamp(input_time)
    output_time = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"
    return (output_time)


def excel_parse(token, org_id, type):
    work_item_mapping = {
        "feature": ("feature", "title_feature"),
        "story": ("user story", "title_story"),
        "bug": ("bug", "title_bug_task"),
        "task": ("task", "title_bug_task")
    }

    df = pd.read_csv('111.csv')
    target_type, title_field = work_item_mapping.get(type, (None, None))

    if not target_type:
        return

    # Фильтруем датафрейм по нужному типу
    filtered_df = df[df['Work Item Type'].str.lower() == target_type]
    total_items = len(filtered_df)

    if total_items == 0:
        logging.info("Нет задач для миграции типа: %s", type)
        return

    # Создаем прогресс бар
    with tqdm(total=total_items, desc=f"Миграция {type}", unit="задача") as pbar:
        for _, row in filtered_df.iterrows():
            attributes = {
                'id': str(row['ID']),
                'work_item_type': row['Work Item Type'].lower(),
                'title_feature': row['Title 1'],
                'title_story': row['Title 2'],
                'title_bug_task': row['Title 3'],
                'assigned_to': row['Assigned To'],
                'state': str(row['State']),
                'created_date': row['Created Date'],
                'description': row['Description'],
                'parent': row['Parent'],
                'projects': row['Projects'],
                'priority': row['Priority'],
                'components': row['Components'],
                'fix_version': row['Fix version'],
                'precondition': row['Precondition'],
                'actual_result': row['Actual result'],
                'repro_steps': row['Repro Steps'],
                'expected_result_description': row['Expected result description']
            }

            migration(token, org_id, attributes, attributes.get(title_field), type)
            pbar.update(1)  # Обновляем прогресс бар


def find_task(token, org_id, parent, key, type):
    url = "https://api.tracker.yandex.net/v2/issues/_search?expand=transitions"
    headers = {
        "Authorization": token,
        "X-Org-ID": org_id,
        "Content-Type": "application/json"
    }

    data = {
        "filter": {
            "queue": "PS",
            "azureId": str(parent)
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        logging.debug(
            "Поиск родительской задачи | Тип: %s | Azure ID: %s",
            type,
            parent
        )

        if type == "story" and response.json()[0]['type']['key'] == "feature":
            logging.info(
                "Найдена родительская задача | Тип: feature | ID: %s",
                response.json()[0]['key']
            )
            set_links(token, org_id, key, response.json()[0]['key'], type)

        elif (type in ["bug", "task"]) and response.json()[0]['type']['key'] == "story":
            logging.info(
                "Найдена родительская задача | Тип: story | ID: %s",
                response.json()[0]['key']
            )
            set_links(token, org_id, key, response.json()[0]['key'], type)

    except requests.exceptions.RequestException as e:
        logging.error(
            "Ошибка поиска задачи | Тип: %s | Azure ID: %s | Ошибка: %s",
            type,
            parent,
            str(e),
            exc_info=True
        )


def set_links(token, org_id, parentkey, key, type):
    url = f"https://api.tracker.yandex.net/v2/issues/{key}/links"
    parentkey = str(parentkey)
    headers = {
        "Authorization": token,
        "X-Org-ID": org_id,
        "Content-Type": "application/json"
    }

    data = {
        "relationship": "relates" if type == "story" else "is parent task for",
        "issue": parentkey
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        logging.info(
            "Задача прилинкована | Тип: %s | Родитель: %s | Дочерний: %s | Тип связи: %s",
            type,
            key,
            parentkey,
            data["relationship"]
        )

    except requests.exceptions.RequestException as e:
        logging.error(
            "Ошибка линковки задачи | Тип: %s | Родитель: %s | Дочерний: %s | Ошибка: %s",
            type,
            key,
            parentkey,
            str(e),
            exc_info=True
        )


def summarize_log(log_file='migration.log'):
    stats = {
        'created': {'total': 0, 'feature': 0, 'story': 0, 'bug': 0, 'task': 0},
        'errors': 0
    }

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'Задача создана' in line:
                    stats['created']['total'] += 1
                    for task_type in ['feature', 'story', 'bug', 'task']:
                        if f'Тип: {task_type}' in line:
                            stats['created'][task_type] += 1

                elif 'ERROR' in line:
                    stats['errors'] += 1

        logging.info("=" * 50)
        logging.info("ИТОГИ МИГРАЦИИ:")
        logging.info("-" * 50)
        logging.info("Всего создано задач: %d", stats['created']['total'])
        logging.info("Создано задач по типам:")
        for task_type, count in stats['created'].items():
            if task_type != 'total':
                logging.info("  - %s: %d", task_type, count)

        logging.info("-" * 50)
        logging.info("Общее количество ошибок: %d", stats['errors'])
        logging.info("=" * 50)

        return stats

    except Exception as e:
        logging.error("Ошибка при подсчете статистики: %s", str(e), exc_info=True)
        return None


if __name__ == "__main__":
    try:
        logging.info("Начало процесса миграции")
        load_dotenv()

        parser = argparse.ArgumentParser(
            description='Миграция задач из Azure в Yandex.Tracker'
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-type',
            choices=['feature', 'story', 'bug', 'task'],
            help='Тип задачи для миграции (feature/story/bug/task)'
        )
        group.add_argument(
            '-log',
            choices=['final'],
            help='Показать итоговую статистику миграции'
        )

        args = parser.parse_args()

        if args.log == 'final':
            summarize_log()
        else:
            token = os.environ["TOKEN"]
            org_id = os.environ["X-ORG-ID"]

            logging.info("Начало миграции задач | Тип: %s", args.type)
            excel_parse(token, org_id, args.type)
            logging.info("Миграция успешно завершена | Тип: %s", args.type)

    except Exception as e:
        logging.error(
            "Критическая ошибка в процессе миграции | Тип: %s | Ошибка: %s",
            getattr(args, 'type', 'unknown'),
            str(e),
            exc_info=True
        )
        sys.exit(1)

