# AWS SQS/SNS broker contract

Attaches alongside `messaging.md`. The cloud-native pair: SQS queues
work, SNS fans out — and the visibility timeout replaces the
heartbeat.

## Eras

Standard versus FIFO queues: FIFO adds ordering per message group
and content-based dedup within a window, at a throughput price;
standard is at-least-once with best-effort order. The choice is
per-queue and priced.

## Idiom

- The visibility timeout is the lease: processing must finish or the
  message returns — set it to the p99 processing time, not the
  average.
- Delete after the work, never before: deletion is the ack.
- Long polling against the empty-receive charge: short polls bill
  the same and return nothing.

## Structure

- Dead-letter queues with redrive policies: max receives before the
  move — and the DLQ monitored, which is the part teams forget.
- SNS fan-out to SQS with filtering policies at the subscription:
  the filter belongs to the subscriber, not the publisher.

## Pitfalls

- At-least-once means duplicates: consumers idempotent by key, per
  the core law.
- FIFO message-group IDs are the parallelism — a hot group ID
  serializes the whole queue's throughput story.
- Retention tops out at 14 days: queues are not archives.
- Poison messages retried forever with no DLQ: the default behavior,
  and the reason the redrive policy exists.
