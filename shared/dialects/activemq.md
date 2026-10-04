# ActiveMQ broker contract

Attaches alongside `messaging.md`. The JMS-era enterprise broker,
with the era visible in the product line itself.

## Eras

Classic versus Artemis — the next-generation broker and now the
default: different store, different threading, same JMS API. The
client code survives the move; the operations do not. Write for the
broker the estate runs; Classic-to-Artemis is a migration brief.

## Idiom

- Queues (point-to-point, one consumer wins) versus topics (pub-sub,
  durable subscribers): the destination type is the delivery
  contract.
- CLIENT_ACKNOWLEDGE and transacted sessions carry the guarantee;
  AUTO_ACKNOWLEDGE is at-most-once wearing a default.
- Durable subscribers for offline topic consumers: their absence is
  silently missed messages, not an error.

## Structure

- Dead-letter policies per broker (Classic) and per address
  (Artemis): the DLQ exists by default — monitored is the part teams
  forget, per the core.

## Pitfalls

- Request-reply over queues: the correlation-ID and reply-to dance is
  a designed protocol, never a convention.
- Virtual topics and composite destinations: features that look
  like pub-sub over queues and behave with sharp edges.
- Store limits under a stopped consumer: the broker's disk, the
  team's outage.
- Selector-heavy consumers: SQL-like filters doing the matching a
  better topic design would make native.
