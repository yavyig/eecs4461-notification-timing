# Final inquiry

How does showing notifications every 10 minutes affect alert timing and waiting time, compared with showing each notice right away?

## Setting and model

The example is one student receiving phone notifications during a 60-minute study session. The apps and student give the project context. The model covers the phone’s waiting list and display rule. See the [ecosystem map](figures/notification-timing-ecosystem-map.png) and the [evidence inventory](evidence/README.md).

The two runs use the same 12 fixed arrival times (E2). The baseline shows each notice when it arrives. The alternative shows all waiting notices together at each 10-minute mark. Arrivals are added before the release check, so a notice that arrives at a batch time can be shown in that batch. An alert moment is a minute in which at least one notice appears.

## Results

| Measure | Immediate delivery | 10-minute batching |
| --- | ---: | ---: |
| Notices shown | 12 | 12 |
| Alert moments | 12 | 6 |
| Average wait | 0 minutes | 5 minutes |
| Longest wait | 0 minutes | 8 minutes |

The two notices that arrived at minutes 3 and 8 appeared together at minute 10 under batching. They waited 7 minutes and 2 minutes. Over the full run, every notice appeared once. See the [immediate trace](../outputs/baseline_raw_00_notification_trace.csv), [batched trace](../outputs/alternative_raw_00_notification_trace.csv), and the [saved outputs](../outputs/) (E4).

## Meaning and next test

Grouping notices gave the model fewer alert moments. The cost was having to wait. A short wait might be acceptable for a routine reminder and more important for a last-minute room change. Those examples show why the same wait can matter differently. The model did not track message urgency, attention, or how a person responded.

A next test could compare more arrival patterns and group intervals. It could also test a rule that lets selected urgent notices appear right away. A separate user study would be needed to learn whether students found the timing helpful.

## Changes since DEL02

DEL03 adds the final explanation, the source and input records, and the editable map. It uses the same model and saved results as DEL02. The earlier release remains available.
