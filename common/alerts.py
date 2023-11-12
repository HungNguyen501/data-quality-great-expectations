"""Alert modules"""
import logging
import traceback

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


def dpd_alert(alert_name, exceptions=(Exception,), suppress=False):
    """ DPD alert decorator """
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                _send_to_telegram(
                    title=alert_name,
                    content=traceback.format_exc(),
                )
                if suppress:
                    logging.warning(f"Suppressed error: {exc}")
                    return None
                raise

        return inner
    return wrapper


def airflow_on_failure_callback(context: Context):
    """Send alert to telegram in case a airflow task failed
    Args:
        context(Context): Airflow context
    """
    _send_to_telegram(
        title=f"***{context['task_instance_key_str']}***",
        content=f"Task {context['task_instance_key_str']} failed!",
    )


def airflow_sla_miss_callback(context: Context):
    """Send alert to telegram in case a airflow task missed SLA
    Args:
        context(Context): Airflow context
    """
    _send_to_telegram(
        title=f"***{context['task_instance_key_str']}***",
        content=f"Task {context['task_instance_key_str']} missed SLA!"
    )
