"""Alert modules"""
from airflow.utils.context import Context
from telegram import Bot
from common.configs import Config, OsVariable


def _send_to_telegram(title: str, content: str):
    """Send alert to telegram channel

    Args:
        title(str): title of alert
        content(str): content of alert
    """
    bot = Bot(token=Config.os_get(key=OsVariable.TELEGRAM_API_TOKEN))
    bot.send_message(
        chat_id=Config.os_get(key=OsVariable.TELEGRAM_CHAT_ID),
        text=f"{title}\n{content}"
    )


def airflow_on_failure_callback(context: Context):
    """Send alert to telegram in case a airflow task failed

    Args:
        context(Context): Airflow context
    """
    _send_to_telegram(
        title=f"***{context['task_instance_key_str']}***",
        content=f"Task {context['task_instance_key_str']} failed!",
    )


def airflow_sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Send alert to telegram in case a airflow task missed SLA
    Args:
        dag: Parent DAG Object for the DAGRun in which tasks missed their SLA.
        task_list: String list (new-line separated, \n) of all tasks that missed
            their SLA since the last time that the sla_miss_callback ran.
        blocking_task_list: Any task in the DAGRun(s) (with the same execution_date
            as a task that missed SLA) that is not in a SUCCESS state at the time that
            the sla_miss_callback runs. i.e. running, failed. These tasks are described
            as tasks that are blocking itself or another task from completing before its
            SLA window is complete.
        slas: List of SlaMiss objects associated with the tasks in the task_list parameter.
        blocking_tis: List of the TaskInstance objects that are associated with the tasks
            in the blocking_task_list parameter.
    """
    _send_to_telegram(
        title=f"***{dag}***",
        content=f"DAG {dag} missed SLA!\n"
                f"dag: {dag}\n"
                f"task_list: {task_list}\n"
                f"blocking_task_list: {blocking_task_list}\n"
                f"slas: {slas}\n"
                f"blocking_tis: {blocking_tis}\n"
    )
