# Juniper JNCIS-DevOps Study Repository

Personal lab material for the **JNCIS-DevOps** (Juniper Networks Certified Specialist – DevOps) certification. The repo covers four core Junos automation topics through working Python scripts, SLAX scripts, YANG modules, and setup guides, all targeting vMX lab devices.

---

## Repository Structure

```
jncis-devops/
├── module-1-advanced-junos-pyez/   # Off-box automation with Junos PyEZ
├── module-2-junos-op-scripts/      # On-box operational scripts (Python + SLAX)
├── module-4-yang/                  # Custom YANG data models and RPC scripts
├── automating-salt/                # SaltStack setup guide for Junos management
└── example_event_script.py         # On-box event-driven automation example
```

---

## Module 1 — Advanced Junos PyEZ

Off-box Python automation using the [Junos PyEZ](https://github.com/Juniper/py-junos-eznc) library, which communicates with devices over NETCONF.

| Script | Description |
|---|---|
| `get_facts_with_cm.py` | Retrieve device facts using a context manager |
| `get_facts_without_cm.py` | Retrieve device facts without a context manager |
| `add_config.py` | Push configuration changes to a device |
| `pyez_load_config_text.py` | Load configuration from a text/set string |
| `pyez_rpc_on_demand.py` | Execute arbitrary NETCONF RPCs on demand |
| `pyez_rpc_on_jxmlease.py` | Execute RPCs and parse results with jxmlease |
| `table_view_example.py` | Extract structured data using PyEZ Tables & Views |
| `junos_add_users.py` | Add user accounts to a Junos device |
| `junos_check_users.py` | Verify configured users on a device |
| `junos_upgrade.py` | Automate Junos software upgrades |
| `start_shell_monitor_traffic.py` | Open a shell session and monitor traffic |

**`jinja2_case_study/`** — Demonstrates config generation with Jinja2 templates and YAML data files. The template (`case1.j2`) renders full Junos interface/BGP/routing-options config blocks from per-device YAML variable files (`vmx-11.yml`, `vmx-12.yml`).

**`myTables/`** — Custom PyEZ Tables & Views defined in YAML (`configTables.yml`) with a Python loader (`configTables.py`) for structured data extraction from Junos operational output.

**Prerequisites:** `junos-eznc`, `jxmlease`

---

## Module 2 — Junos Op Scripts

On-box operational scripts that run directly on the Junos CLI.

**Python scripts (on-box):**

| Script | Description |
|---|---|
| `helloworld_on-box.py` | Basic on-box Python hello world |
| `interface_bounce.py` | Disable then re-enable an interface after a configurable delay |
| `interface_show.py` | Display interface information and address family details |
| `arguments.py` | Demonstrates passing arguments to on-box scripts |

**SLAX scripts** (XSLT-based Junos scripting language):

| Script | Description |
|---|---|
| `helloworld.slax` | Basic SLAX hello world |
| `helloworld_hidden_args.slax` | Op script with hidden argument definitions |
| `helloworld_visible_args.slax` | Op script with visible/documented arguments |
| `bgp-sum.slax` | Display a BGP summary |
| `interface_info.slax` | Retrieve and display interface information |
| `interface_bounce.slax` | Bounce an interface via SLAX |
| `interface_request.slax` | Issue interface-related requests |
| `diff_slax_outputs.slax` | Compare outputs between two SLAX script runs |

---

## Module 4 — YANG Data Modelling

Custom YANG modules and Python scripts that exercise Junos YANG-defined RPCs.

| File | Description |
|---|---|
| `rpc-interface-status.yang` | YANG module defining a custom `show intf status` RPC using Junos ODL extensions |
| `rpc-interface-status.py` | Python script invoking the custom interface status RPC |
| `sr.yang` | YANG module modelling static route configuration (`prefix` + `next-hop`) |
| `sr.py` | Python script exercising the static route YANG model |

---

## Automating with SaltStack

`automating-salt/README.txt` is a step-by-step lab guide covering:

1. **Salt installation** — bootstrap script setup for master and minion servers
2. **Basic Salt configuration** — connecting minions to the master, key acceptance, remote execution (`test.ping`, `cmd.run`)
3. **Junos proxy minions** — managing Junos vMX devices via Salt using proxy minion processes (NETCONF/PyEZ under the hood), including pillar configuration for device credentials and the Salt top file

---

## Event-Driven Automation

`example_event_script.py` — An on-box event script that fires in response to Junos syslog events. It logs the trigger event context and raw XML data to a file, demonstrating how to use the `Junos_Context` and `Junos_Trigger_Event` built-ins.

---

## Lab Setup

### Topology

Scripts target a two-node vMX lab (`vmx-11` / `vmx-12`):

- **Host:** `172.25.11.1` (single-device scripts) / `vmx-11`, `vmx-12` (multi-device scripts)
- **User:** `brook`

### Credentials

Module 1 (PyEZ) scripts read device credentials from environment variables. A template is provided at the repo root:

```bash
cp lab.env.example lab.env
```

Edit `lab.env` and fill in your values:

```bash
export JUNOS_HOST=172.25.11.1   # target device IP or hostname
export JUNOS_USER=brook          # SSH username
export JUNOS_PASSWD=             # SSH password (leave blank if using SSH keys)

export NEW_USER_PASSWD=          # used by junos_add_users.py only
```

Then source the file before running any script:

```bash
source lab.env
python get_facts_with_cm.py
```

`lab.env` is listed in `.gitignore` and will never be committed.

---

## Dependencies

Install Python dependencies via:

```bash
pip install -r requirements.txt
```

For the SaltStack module, follow the installation steps in `jncis-devops/automating-salt/README.txt` — Salt is a system-level install and is not included in `requirements.txt`.
