# Implementation and representation notes

The preserved Mesa Boltzmann Wealth Model supplies an agent/model/DataCollector structure. The notification adaptation replaces its represented phenomenon and state-update rules. Notification agents represent notification records, not people. The single-recipient study-session context is an environmental boundary, not a behavioural simulation.

The formative feedback in the local DEL01 feedback PDF confirmed the deployed observable referent, outputs, boundary, and separation from distraction/wellbeing claims. It asked for a clear distinction between documented iOS controls and the synthetic model's fixed batch intervals and alert-counting rule. DEL02 narrows the broader proposal to immediate delivery versus fixed 10-minute batching, with one deterministic dispersed trace. Urgent bypass, urgency/deadline outcomes, alternative intervals, and clustered arrivals are deferred.

The baseline and alternative share all settings except `delivery_mode`. There is no random result variability. Consequential ordering is explicit: admit every arrival at the current minute, then release the pending queue if due. Thus an arrival exactly on a release boundary has zero presentation delay. Multiple notifications released together count as one model-defined alert episode. This metric does not establish that an actual person noticed or acted on an alert.

The primary outputs are the two notification traces and two minute-by-minute state traces. Summary CSVs and timeline PNGs are derived by reading those saved primary outputs. Independent arithmetic in the tests verifies the 10-minute release boundaries. Conservation is checked at every recorded minute.

The publication repository is https://github.com/yavyig/eecs4461-notification-timing. The submission version is identified by the annotated `DEL02` tag and `DEL02 Release`. The practical verification record is in `verification.txt`. The eClass report and Individual Accountability Record are separate from this code publication.

AI provenance: Codex drafted the adaptation, test cases, documentation, and plotting code. Execution checked the stated results. Source example preservation was checked against downloaded upstream files, and the source example was executed with conservation checks. This record must not be described as grammar-only AI assistance.
