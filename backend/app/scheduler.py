"""
Background scheduler for periodic metrics collection.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from .services.metrics_collector import collect_metrics, cleanup_old_metrics

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Initialize and start the background scheduler."""

    # Collect metrics every 5 minutes
    scheduler.add_job(
        collect_metrics,
        trigger=IntervalTrigger(minutes=5),
        id='collect_metrics',
        name='Collect database metrics',
        replace_existing=True
    )

    # Cleanup old metrics daily at midnight
    scheduler.add_job(
        cleanup_old_metrics,
        trigger='cron',
        hour=0,
        minute=0,
        id='cleanup_metrics',
        name='Cleanup old metrics',
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started: metrics collection every 5 minutes, cleanup daily")


def stop_scheduler():
    """Stop the background scheduler."""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
