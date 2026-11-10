# Notification presentation timing prototype

This DEL02 prototype compares immediate delivery with fixed 10-minute batching for the same 12 synthetic notifications in a 60-minute session. It is a runnable Mesa adaptation, not an implementation of iOS Scheduled Summary.

Repository: https://github.com/yavyig/eecs4461-notification-timing

The submission version uses the annotated tag `DEL02` and the release title `DEL02 Release`. Publishing the code does not submit the separate eClass report or Accountability Record.

## Requirements and installation

Tested with Python 3.12.14 on Windows and Mesa 3.5.1. Use Python 3.12 or later. From this directory:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`. The project uses no account credentials, network data, private messages, or configuration files. Internet access is needed only when installing packages. The pinned top-level dependencies are in `requirements.txt`; their transitive dependencies are resolved by pip.

## Preserved Mesa example

The source example is Mesa's **Boltzmann Wealth Model**, version 3.5.1. All six upstream example files are preserved unchanged under `src/boltzmann_wealth_model/`, with the upstream licence and `SOURCE.md` recording the URL, commit, access date, and SHA-256 hashes.

Run the preserved local model and agents for ten steps:

```text
python run_source.py
```

The wrapper loads the preserved local files under the module names used by their unchanged upstream imports. It prints a Gini value and checks that the 100 agents retain a total of 100 units of wealth. That Gini value is random and is unrelated to the notification comparison. The optional upstream Solara and Streamlit interface files are preserved, but the required source verification command above uses the model without a browser. Streamlit is not a project dependency and its optional interface was not tested.

## Adapted project model

```text
python -m src.project_model.run
```

Run that command from the directory containing this README. It writes the baseline and alternative files to `outputs/`. An optional `--output-dir PATH` argument chooses a different output directory. Existing files with these output names are replaced on a rerun.

The adaptation in `src/project_model/` retains the source example's separation between agents and model, Mesa agent activation, and `DataCollector`. It replaces wealth, grid movement, random exchanges, and Gini with notification agents, a shared pending queue, presentation timing rules, and count/delay outputs. These changes implement a different focal activity; the source example supplies software structure rather than evidence about notifications.

- Each `NotificationAgent` moves from `scheduled` to `pending` at its arrival minute and then to `presented` when the delivery rule releases the queue.
- One model step advances one minute. Recorded minutes run from 0 through 60 inclusive. Arrivals are admitted before releases at the same minute.
- Baseline `delivery_mode="immediate"` releases pending notifications immediately. Alternative `delivery_mode="batch"` releases them at multiples of the fixed `batch_interval=10`.
- Multiple notifications presented at one timestamp count as one alert episode. An empty queue produces no alert episode. A final horizon flush is defined, although minute 60 is already a batch boundary in the reported run.
- Arrivals are `3, 8, 12, 17, 22, 28, 33, 38, 42, 47, 52, 58`. There is no random arrival generation. `delivery_mode` is the only changed comparison condition; arrivals, horizon, batch interval setting, processing order, and metrics are identical.

## Outputs

Each condition produces the following four files, with `baseline` or `alternative` replacing `CONDITION`:

| File | Contents |
| --- | --- |
| `CONDITION_raw_00_notification_trace.csv` | One row per notification, containing arrival minute, presentation minute, delay, final state, and release count |
| `CONDITION_raw_01_state_by_minute.csv` | Mesa DataCollector records for all 61 minutes, including scheduled, pending, and presented counts and cumulative alert episodes |
| `CONDITION_processed_00_summary.csv` | Notification count, distinct presentation timestamps, and mean and maximum delay, calculated from the saved notification trace |
| `CONDITION_processed_01_presentation_timeline.png` | A readable timeline generated from the saved trace; circles mark arrivals, vertical marks show presentations, and horizontal segments show delays |

The baseline produces 12 alert episodes, zero mean delay, and zero maximum delay. The alternative produces 6 alert episodes, 5 minutes mean delay, and 8 minutes maximum delay. Both present all 12 notifications exactly once. These are conditional model results for the specified synthetic trace.

## Verification

```text
python -m unittest discover -s tests -v
```

Six checks cover exact batch boundaries, simultaneous arrivals, horizon flushing, empty queues, conservation, no early or duplicate release, independently calculated presentation times, and invalid arrivals. Run the source command, project command, and tests after installation. `docs/verification.txt` records the local and fresh-environment checks. To verify the release, download the `DEL02` source archive, extract it, and follow these installation and run commands from the extracted directory. Release notes record the released-file check.

## Limits and next work

The current slice includes no human agent, attention measure, app content, network latency, interruption levels, urgency labels, deadlines, or authorized urgent bypass. It uses one recipient context and one deterministic dispersed arrival trace. User behaviour, actual iOS internal scheduling, and wellbeing or productivity are not represented. The fixed interval and alert-counting rule are explicit modelling assumptions.

Next work can add clustered arrivals, compare intervals of 5, 15, and 30 minutes, then introduce urgency labels and an independently controlled user-authorized bypass. The DEL02.1 report contains the fuller inquiry, evidence, representation choices, interpretation, and rationale. This README is the practical run guide.
