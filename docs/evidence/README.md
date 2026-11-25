# Evidence and model inputs

| ID | Source or input | Status | How it was used | Limit |
| --- | --- | --- | --- | --- |
| E1 | [Apple. (n.d.). Change notification settings on iPhone. *iPhone User Guide*.](https://support.apple.com/guide/iphone/change-notification-settings-iph7c3d96bab/ios) | Documented feature | Shows that users can choose apps and times for Scheduled Summary. | The guide does not establish the internal rules or a fixed 10-minute interval. |
| E2 | [Synthetic arrival record](synthetic-arrivals.csv) and [model rules](../../src/project_model/model.py) | Synthetic model input | Gives both runs the same 12 arrivals and a 60-minute window. | The arrivals are examples. They were not collected from a phone. |
| E3 | [Project Mesa. (2026). *Boltzmann Wealth Model* (Mesa 3.5.1) [Source code].](https://github.com/mesa/mesa/tree/e733e8ecb2a162a552c815205da9503d1ed7ce16/mesa/examples/basic/boltzmann_wealth_model) | Published code example | Supplies the model, agent, and data collection structure. | The example models wealth and does not supply notification behaviour. |
| E4 | [Saved traces and summaries](../../outputs/) from the [DEL02 Release](https://github.com/yavyig/eecs4461-notification-timing/releases/tag/DEL02) | Simulation output | Records when notices appear and how long each one waits. | These results come from one synthetic session. |

The CSV in this folder records the input minutes defined in the model. Run the model from the repository root to reproduce the outputs. The simulation does not read this CSV as a runtime input.
