# IBM MQ broker contract

Attaches alongside `messaging.md`. The oldest broker still running
the world's money: queue managers, channels, and exactly-once
habits earned decades before the term existed.

## Eras

MQSeries to WebSphere MQ to IBM MQ — the same wire discipline under
new names. The era markers are practical: persistent messages and
syncpoint are the durability contract; the platform (z/OS versus
distributed) decides assumptions worth checking.

## Idiom

- Queue manager, queue, channel: the topology is configured
  infrastructure — object definitions are code and versioned like
  code.
- Persistent messages with syncpoint for exactly-once-shaped work:
  the unit of work commits or rolls back as one.
- Model queues declare the template; dynamic queues are
  per-conversation, and their lifetime is part of the contract.

## Structure

- The dead-letter queue is system-level and always on: poison
  handling routes there — monitoring it is the core's dead-letter
  discipline made native.

## Pitfalls

- Non-persistent messages promising more than they deliver: state
  the guarantee per message.
- Channel retry and reconnection storms: tuned intervals, or the
  network dies of politeness.
- Backout counts and threshold queues: the per-queue retry contract
  — unset, a poison message loops.
- Message formats and headers transformed between systems: the
  serialization boundary rules apply to envelope and body both.
