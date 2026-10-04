# Solace broker contract

Attaches alongside `messaging.md`. PubSub+: the enterprise backbone
where guaranteed delivery is the product, and the VPN is the
tenancy.

## Idiom

- Two delivery modes, decided per message: direct (fast, best-effort)
  versus guaranteed (spooled, acknowledged, replayable) — the
  guarantee is per-topic and stated, never defaulted.
- Message VPNs are the tenancy boundary: naming, ACLs, and spooling
  are per-VPN; an integration across VPNs is a design decision, not
  a config copy.
- Topics are hierarchical with wildcards: the subject space is
  designed like a namespace, and subscription matching is the API.

## Structure

- Durable queues and topic-to-queue bindings on the consuming side:
  the queue survives the consumer; the binding survives both.
- Replay from spool is a designed capability — window and
  eligibility configured, the core's replay policy applied.

## Pitfalls

- Direct messaging promoted to guaranteed silently: the guarantee
  changed and nobody wrote it down.
- Spool limits under a stopped consumer: guaranteed delivery becomes
  guaranteed refusal.
- MQTT and REST bridges translating semantics: QoS levels and ack
  models differ — the boundary rules apply at every bridge.
- Egress shutdowns as flow control: a shutdown is a backpressure
  event, not an outage — know which one you are having.
