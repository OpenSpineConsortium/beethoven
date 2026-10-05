# Site modules: where the protocol ends and a university begins

greg asked on 2026-10-04 at 23:46Z to separate the protocol from the specifics of Wayne State's grid
as far as possible while keeping what it does, to put every Wayne State detail into its own module
that another university replaces with its own, to research a sound abstract way to draw that line, to
file the gaps as Linear issues and to start on them. This is the result: the model (sections 1 and
2), the research behind it (3), Wayne State written as a module (4), how a module is shown to work
(5 and 6), the gaps by repository with their issues (7), the order and owners (8), and two decisions
with defaults (9).

Linear: project *U — University Site Modules*, BEE-198 to BEE-222. Written by the site-module thread,
2026-10-05; checked against each repository's `main` of 2026-10-04. Beethoven runs Claude Code and is
not an Anthropic product; "Claude" and "Claude Code" are Anthropic's marks, used here to say what it
runs; "Open OnDemand" is the mark of its publisher.

## 1. The answer

Beethoven's protocol is already mostly site-neutral at its core: hpcworker reads one site profile
(`framework/profiles/wayne.json`), drives the scheduler through an eight-call adapter interface, and
the clients carry the profiles as data. What is missing is not a mechanism but a boundary that is
drawn on purpose and enforced by tests. Today Wayne State leaks out of the profile in five ways:
values written into code (the bridge's `grid.wayne.edu:22`, `DEFAULT_SITE = 'wayne'`, the
`/rs/rs_grp_oschome` image path in bee), behaviour that only fits Wayne State's kind of portal, VPN,
two-factor prompt and scheduler, sentences a student reads ("A Wayne State grid account",
"GlobalProtect"), rules whose source is not recorded, and tests that only ever load `wayne.json`.

The design below makes a **site module** the one place a university lives, and makes the core prove
it does not need Wayne State:

1. **Three layers, each owned by someone different.** The *product* (Beethoven's own rules and
   defaults, in code), the *site* (the university's cluster: scheduler, hosts, portal, VPN, second
   factor, login-node policy, the words students see), and the *lab* (one group's deployment on that
   cluster: its volume, shared copy, images, approved list). Wayne State today is one site module plus
   one lab module (`oschome`). A second Wayne State lab writes only a lab module; a new university
   writes a site module and a lab module.
2. **Modules are data, never code.** Every way two universities can *behave* differently is a closed
   list of choices implemented in the core (scheduler `slurm|pbs|lsf`, portal sign-in
   `http-basic|cookie`, second factor `totp|duo|none`, access list `posix-acl-root|group|none`, ...).
   A module picks one and gives its parameters. A university the list does not cover needs a reviewed
   core change, not code in its module. This keeps "no remote code" true for the extension and lets a
   module be validated before anything runs it.
3. **One composed profile is what every consumer reads.** hpcworker composes product defaults, the
   site module and the lab module into `profiles/<id>.json`, the file the extension and the desktop
   edition already vendor and the engine (BEE-219) and the VS Code edition (BEE-217) will. The first
   step changes no behaviour:
   the composed Wayne State profile must parse equal to today's `wayne.json`, and be byte-equal to it
   once a commit that changes only formatting has put today's file in the composer's key order.
4. **A second, synthetic site proves the boundary.** An `example` site module that differs from Wayne
   State wherever a module can (a required allocation account and no QoS, node-local
   `$SLURM_TMPDIR`, a Lustre home, Singularity, a cookie-sign-in portal, Duo, no VPN, no shared copy,
   group-based access) runs through every test suite beside Wayne State's, and a lint derived from the
   modules' own values fails any core file that spells a site's host, path, partition or link. It
   keeps Slurm, since the PBS and LSF adapters already have fixture tests of their own
   (`framework/tests/test_adapters.py`).

## 2. The model

### 2.1 What varies between universities, and how each kind is expressed

| Kind of variation | Examples at Wayne State | Expressed as | Where the behaviour lives |
|---|---|---|---|
| Value | `submit_host` warrior, `node_tmp`, partitions and QoS, `ssh_host_key`, help links | a field | the core reads it |
| Alternative | Slurm; portal sign-in by HTTP basic; Google Authenticator codes; GlobalProtect; POSIX ACL on the volume root | an enumerated choice with parameters | one implementation per choice, in the core |
| Optional feature | `vpn_required`, `shared_install`, `scheduler_in_worker`, the ssh path, requeue | a boolean or the field's presence | the core, switched by the module |
| Words (the "theme") | "AccessID", "the grid", "GlobalProtect", "Google Authenticator", `hpc@wayne.edu`, "Wayne State grid" | the site's nouns, and its own wording for any sentence it must change, keyed against the core's catalogue | the core's catalogue of sentences; a key the site leaves out falls back to the core's wording; placeholders come from a declared set a test checks |
| Policy with its source | 20 processes on the login node (Wayne State's published policy), no container commands on warrior (C&IT, 2026-09-28), the banned commands in warrior's `/etc/motd` | a rule with `value`, `source`, `stated_by`, `date` | the core enforces the strictest of product and site |
| Measured fact | egress results, the host key, the Slurm binds measured on asx1, `ood_auth` | a record in the module's `facts/`, apart from its declarations: `{value, when, where, how}` | the probe job measures again; a measurement never replaces a declaration, and a disagreement is reported for a person to resolve; "not yet measured" is a legal state |

### 2.2 The three layers

**Product** (in code, not in any module): the credential rules, the 60 s poll floor and the wall-time
rule (this product's own etiquette, which C&IT never stated), `claude_config_dir`
(`$HOME/.beethoven/claude`) and the consent markers, `login_abandon_s` 1200, `ipc_dir` `/dev/shm`, the
worker defaults a lab has not overridden, and the rule that node-local temp is never trusted blindly.
A site may make a product rule stricter (a 120 s floor), never looser.

**Site** (a university's cluster, whoever uses it):

- identity and matching: `site`, `display_name`, `match` (the portal origins and ssh hosts that
  identify the site; replaces the extension's guess from the second DNS label);
- scheduler: `scheduler`, `submit_host`, `bin_dir`, the partition and QoS catalogue,
  `partitions_gpu`, `max_walltime`, whether requeue is offered (an explicit flag, not "the QoS is
  named requeue");
- nodes and storage: `node_tmp`, `node_tmp_var`, `tmpdir_is_node_local`, `home_filesystem`,
  `cache_dir`, `xdg_runtime_fix`;
- runtime: `runtime`, `runtime_module`, `runtime_bin`, `fakeroot_rung`, `scheduler_in_worker` with the
  measured bind set (today written into `lib/adapters/common.sh`);
- network and sign-in: `egress`, `vpn` (required, app, portal, help and store links), `portal` (Open
  OnDemand, its sign-in kind, start page, shell path), `ssh` (host, port, pinned key, relay, the
  options it needs such as `hmac-sha1`), `second_factor` (kind, prompt and refusal wording, setup
  route, help and store links), `account_id` (its name "AccessID", pattern, example, e-mail domain);
- rules: the login node's process cap, banned commands and anything else the university states, each
  with its source; the jurisdiction's data rules (PHI, FERPA) as text;
- texts: the site's words for the student-facing bundle.

**Lab** (one group's deployment on a site): `lab`, `shared_state_dir`, `shared_install`, `image_store`,
`claude_bin`, the volume `binds`, `account` (allocation), the engine's image directory, the access list
(`access: {kind, root, ...}`), the lab's choice of partition for long workers (and the all-queue list
the desktop thread is adding as `worker_race`), `browser_key_days`, `restricted`,
`restricted_workspaces`, `worker_defaults`, and the lab's own texts (who the lab lead is, how to ask).

Later, the single partition fields become role lists: `short`, `worker` and `gpu`, each an ordered
list of `{partition, qos}` the core may try, as ReFrame's `access` list does per partition. The site
says which partitions and QoS exist; the lab says which it uses for each role. `worker_race` is the
first such list.

greg's base decision D3 (2026-10-05 00:28Z) drops GPU workers from hpcworker unless a student uses
them. The site module still lists its GPU partitions (`partitions_gpu`), because the engine's own
jobs (training, evaluation) choose from that catalogue; a lab module that offers no GPU worker simply
has no `gpu` role, and the launcher reads only the roles a lab gives it.

**Account** (the student's `~/.hpcworker/profile.json`): only the student's own choices. Today the file
is a full copy made at install, and only 16 `FIELDS_FROM_SITE` follow the site file afterwards, so a
renamed partition stays wrong in every account installed before the rename. Site- and lab-owned fields
should always come from the module at read time.

Each schema field names its owner and who may override it. Validation refuses a lab module that sets a
site-owned field (`ssh_host_key`) and a site module that sets a lab-owned one (`shared_state_dir`). A
scalar set in a later layer replaces an earlier one; a list such as `binds` adds to it (the product's
`$HOME`, then the lab's volumes). `profile.py show --layers <id>` prints every composed value with the
layer and the file that set it, as `spack config blame` does.

### 2.3 When each choice is bound

| Binding time | What happens | Who |
|---|---|---|
| Module authoring | site and lab modules written and validated; the conformance suite passes | the maintainer or a lab lead |
| Framework release | hpcworker composes `profiles/<id>.json`; `deploy_shared.sh` publishes the copy | the maintainer |
| Client build | the extension, desktop and VS Code editions and the engine vendor the composed profiles as data; the bridge's built-in allow list is generated from them | the maintainer's build |
| Install | `hpcworker install --shared` points an account at its deployment | the student, through a client |
| Run | the client matches the portal origin or ssh host to a deployment; the job reads the profile; the probe re-measures | automatic |

### 2.4 Where modules live

In hpcworker, beside the profiles they replace: `framework/sites/<site>/site.json`,
`framework/sites/<site>/labs/<lab>.json`, `framework/sites/<site>/README.md` (who runs the
cluster, where each value came from; `docs/WAYNE_STATE_PILOT.md` moves here), `framework/sites/<site>/fixtures/`
(scheduler output captured at that site), `framework/sites/<site>/facts/` (what was measured there,
when, where and how) and `framework/sites/<site>/expect.json` (what the tests should see for this
site). `framework/profiles/<id>.json` stays as the composed output, so nothing that
vendors profiles today has to change on the first day. A separate repository is not needed yet: the
engine and the clients take the composed profiles as data, which is allowed across the dependence
line, and a later move would be a `git mv` plus one changed path in each `pull.sh` (decision BEE-221, section 9).
greg decided BEE-221 on 2026-10-05 at 00:59Z for a repository of their own, `beethoven-sites`: the
paths above are then that repository's `sites/<site>/...`, and hpcworker's `framework/sites/` is its
pinned copy (section 9).

## 3. Why this line

The research read the primary text of each tool's documentation or source where the network allowed;
what was seen only in a search excerpt is marked "not verified".

### 3.1 Mechanism in the core, policy in the module

Hydra's designers made the separation of mechanism and policy "a basic design principle", building "a
kernel composed (almost) entirely of mechanisms" (Levin, Cohen, Corwin, Pollack and Wulf,
"Policy/mechanism separation in Hydra", SOSP 1975, https://doi.org/10.1145/800213.806531; abstract
not verified on the ACM page, which the session could not reach; Wulf et al., "HYDRA: the kernel of a
multiprocessor operating system", CACM 17(6), 1974, https://doi.org/10.1145/355616.364017). Here the
mechanism is everything a worker does the same way everywhere (the job's lifecycle, the contract
files, the gate's lines, the credential rules, the poll floor); the policy is what a university or a
lab decides (which partition, which paths, which second factor, what students are told). The test of
the line: a second university should need a new policy, never a new mechanism, unless it really does
something no supported university does.

### 3.2 Variation points and when they are bound

Software product-line engineering treats each place two products may differ as a *variation point*
with a set of *variants* and a *binding time* (Pohl, Böckle and van der Linden, *Software Product
Line Engineering*, Springer 2005, https://doi.org/10.1007/3-540-28901-1; FODA classifies features by
compile-time, load-time and run-time binding, Kang et al., CMU/SEI-90-TR-21, 1990; Svahnberg, van
Gurp and Bosch, "A taxonomy of variability realization techniques", Software: Practice and
Experience 35(8), 2005; all three not verified on the page). Section 2.1's table is that
classification applied to Wayne State's details, and section 2.3 is the binding-time table. Naming the
kind of each variation decides how it is expressed: a value is a field, an alternative is an
enumerated choice whose implementations live in the core, words are a catalogue, a measured fact is a
record.

### 3.3 Ports and adapters

Cockburn's hexagonal architecture lets an application "be developed and tested in isolation from its
eventual run-time devices" behind ports with one adapter per device (2005,
https://alistaircockburn.com/Hexagonal-Architecture; quotation not verified on the page); Martin's
dependency inversion puts both sides on an abstraction (C++ Report, 1996). hpcworker already has one
port, the scheduler, with Slurm, PBS and LSF adapters. The design adds the others a university varies
along: container runtime, portal sign-in, second factor, network reach, node-local storage, access
list. A site module selects an adapter by name; it never supplies one.

### 3.4 How HPC tools draw the same line

| Tool | Unit of site | How the site is chosen | Layers | How a site config is checked |
|---|---|---|---|---|
| ReFrame | `systems[]` with `partitions[]`, each naming its `scheduler`, `launcher` and an `access` list of scheduler options | `hostnames` regular expressions matched against the host name; a built-in `generic` system matches anything | built-in file, then files on `RFM_CONFIG_PATH`, then `-C` files; command line over environment over files | validated against `schemas/config.json`; `--show-config` prints the merged value |
| nf-core/configs | `conf/<site>.config` plus `docs/<site>.md`, each with a description, contact and URL | the user names it, `-profile <site>` | the pipeline's config, then the institutional one; pinnable version; a local path works offline | CI fails if a registered profile is missing from the test matrix; each profile is loaded and printed, no job run |
| Open OnDemand | `clusters.d/<id>.yml`: `metadata`, `login`, `job.adapter` (slurm, pbs, lsf...), `batch_connect`, and a schema-free `custom` | the file's name; apps name cluster ids | site overrides of an app kept in `/etc/ood/config/apps/<app>`, apart from the app, so either updates alone | `rake test:jobs:<cluster>` submits a real one-minute job per cluster |
| Parsl | a `Config` of executors, each a *provider* (how resources are requested) and a *launcher* (how workers are placed) | the user's script; per-site examples ship in `parsl/configs/` | none beyond the script | "examples must be customized for the user's allocation" |
| dask-jobqueue | `jobqueue.yaml`, one section per scheduler | the cluster class | `/etc/dask/` (the site's, "will affect all people on the cluster") under `~/.config/dask/` under keyword arguments | none stated |
| PSI/J | a core `JobSpec` "independent of how and where" it runs; one executor per scheduler | `JobExecutor.get_instance('slurm')` | site specifics only through prefixed `custom_attributes` (`slurm.constraint`) | sites contribute scheduled test runs to an aggregation service |
| Spack | configuration scopes | precedence | defaults < system < site < user < environment < command line; `::` replaces a lower scope; `spack config blame` shows each value's file | editors validate against JSON Schema |
| Lmod | `SitePackage.lua` (hooks) outside the install | `LMOD_PACKAGE_PATH` | `LMOD_SITE_MSG_FILE` replaces some or all messages; `LMOD_SITE_NAME` is the site, "not the name of the cluster" | none stated |
| Globus Compute | an endpoint's `config.yaml` from a Jinja template | the endpoint | the administrator's template and the user's variables | a JSON schema the administrator writes; `additionalProperties: false` rejects unexpected keys |

Sources: the projects' repositories on GitHub (reframe-hpc/reframe, nf-core/configs and nf-core/tools,
OSC/ood-documentation, Parsl/parsl, dask/dask-jobqueue, ExaWorks/psij-python and job-api-spec,
spack/spack, TACC/Lmod, globus/globus-compute), read 2026-10-04.

What the design takes from them: an explicit list a site declares to be matched against (ReFrame's
`hostnames`, Open OnDemand's file name), instead of the extension's guess from the second DNS label;
layers with a "which layer set this" view (Spack's scopes and `blame`; dask's `/etc` under the user's
file); a role-to-scheduler-options list per partition (ReFrame's `access`), which is where
`worker_race` points; a schema that refuses unexpected keys when a module is written (Globus Compute),
while consumers of a composed profile keep ignoring unknown fields across versions as hpcworker does
today; a CI check that every registered site is in the test matrix (nf-core's checker); and a real job
per site as the second tier (Open OnDemand's `test:jobs`, PSI/J's site runs).

What it leaves: code in a site module (Lmod's `SitePackage.lua`, nf-core's configs, which are Groovy
and can run `sacctmgr`), because the extension may run no code it did not ship and a module is easier
to check when it is only data; and fetching the site's configuration when a run starts (nf-core loads
it from GitHub by default), because the clients bundle profiles at build time and the bridge's allow
list is a security boundary that must not widen at run time.

### 3.5 The words a student reads

A resource bundle "of last resort" answers any key a more specific bundle lacks (OpenJDK
`ResourceBundle`); Open OnDemand sites override its `locales/en.yml`, and it warns that "attempting to
use a variable that is not available to the translation will crash the application"; Lmod lets a site
replace "some or all" of its messages. So the core keeps the catalogue of sentences, a site supplies
only its nouns and the sentences it must change, a missing key falls back to the core's wording, and
the placeholders a sentence may use are a declared set checked by a test.

### 3.6 What is declared and what is measured

Ansible keeps site-supplied facts in their own namespace "so variables will not override each other";
Spack's `external find` "does not overwrite existing entries"; ReFrame uses a declared processor as
given, then a cached detection, then detects, and only warns when detection fails. The profile today
mixes declarations with measurements (`egress.measured`, the host key measured from the internet, the
Slurm binds measured on asx1, dates inside `notes`). The design keeps measurements as records apart
from declarations, never lets a measurement silently replace a declaration, reports a disagreement
for a person to resolve, and treats "not yet measured" as a legal state.

### 3.7 Conformance

A plug-in proves it fits by passing the host's test kit: Kubernetes' `csi-sanity` checks a storage
driver "conforms to the CSI specification" and skips what the driver does not advertise
(`Skip("GetCapacity not supported")`); Java's TCK plays the same part for a specification (not
verified on jcp.org). For a site module that is two tiers: everything that needs no cluster runs in CI
for every module (schema, composition, texts, the per-site test runs, the literal lint), and a probe
job on the site compares declarations with measurements, skipping what the module does not declare.

## 4. Wayne State as a module

A sketch of the two files; field names are the current schema's where one exists. The composed
`profiles/wayne.json` must stay byte-identical to today's until a consumer is ready for a change.

```json
// framework/sites/wayne/site.json
{
  "kind": "site", "module_version": 1, "site": "wayne",
  "display_name": "Wayne State University HPC grid",
  "match": { "portal_origins": ["https://ondemand.grid.wayne.edu"], "ssh_hosts": ["grid.wayne.edu:22"] },
  "scheduler": "slurm", "submit_host": "warrior",
  "partition_cpu": "secp", "qos_cpu": "secondary",
  "partition_cpu_batch": "reqp", "qos_batch": "requeue", "requeue": true,
  "partitions_gpu": ["gmsap", "gvohp"],
  "node_tmp": "/tmp/$USER/hpcworker_$SLURM_JOB_ID", "tmpdir_is_node_local": false,
  "runtime": "apptainer", "runtime_module": "apptainer/1.2.2", "runtime_bin": "...",
  "scheduler_in_worker": { "enabled": true, "binds": ["/usr/bin/sbatch", "..."] },
  "ssh_host": "grid.wayne.edu", "ssh_port": 22, "ssh_host_key": "SHA256:...", "ssh_options": ["MACs=+hmac-sha1", "AddressFamily=inet"],
  "portal": { "kind": "ood", "base_url": "https://ondemand.grid.wayne.edu", "auth": "http-basic", "start_page": "/public/start.html" },
  "vpn": { "required": true, "app": "GlobalProtect", "portal": "protect.wayne.edu", "help_url": "...", "store_links": {} },
  "second_factor": { "kind": "totp", "app": "Google Authenticator", "help_url": "...", "setup": "ood-app:2FA Setup", "refusal_pattern": "..." },
  "account_id": { "name": "AccessID", "pattern": "^[a-z]{2}[0-9]{4}$", "example": "ab1234" },
  "rules": {
    "login_node_max_processes": { "value": 20, "source": "https://services.wayne.edu/TDClient/277/Portal/KB/ArticleDet?ID=20254", "stated_by": "Wayne State's published policy" },
    "login_node_no_containers": { "value": true, "stated_by": "C&IT", "date": "2026-09-28" },
    "login_node_banned_commands": { "value": ["python3", "node", "make", "md5sum", "rsync", "..."], "source": "warrior /etc/motd (23 names, today in tests/test_login_node.py)" }
  },
  "texts": { "cluster_noun": "the grid", "site_name": "Wayne State", "session_title": "Wayne State grid", "help_contact": "hpc@wayne.edu" }
}
```

```json
// framework/sites/wayne/labs/oschome.json
{
  "kind": "lab", "module_version": 1, "site": "wayne", "lab": "oschome",
  "shared_state_dir": "/rs/rs_grp_oschome/$USER/hpcworker",
  "shared_install": "/rs/rs_grp_oschome/shared/beethoven/hpcworker/current",
  "image_store": { "type": "sandbox", "path": "/rs/rs_grp_oschome/shared/beethoven/containers/claude-node22" },
  "claude_bin": "/rs/rs_grp_oschome/shared/beethoven/npm-claude-node22/bin/claude",
  "binds": ["/rs/rs_grp_oschome/$USER", "/rs/rs_grp_oschome/shared/beethoven"],
  "containers_dir": "/rs/rs_grp_oschome/shared/beethoven/containers",
  "access": { "kind": "posix-acl-root", "root": "/rs/rs_grp_oschome" },
  "worker_defaults": { "cpus": 2, "mem": "8G", "hours": 8, "permission_mode": "default", "capacity": 4 }
}
```

`$HOME` in today's `binds` and `claude_config_dir` are product values and leave the module. What
was measured (the Slurm binds on asx1 on 2026-09-28, the egress results, the host key read on
2026-10-02, the portal's sign-in kind seen on 2026-10-01) moves to `framework/sites/wayne/facts/`, one
record per measurement, and the dates leave `notes`.

## 5. How a module is shown to work

1. **Schema per layer**, in `lib/profile.py` (Python 3.6, the login node's), with each field's owner;
   the composed profile validates as today.
2. **Golden composition**: `compose(sites/wayne/site.json, labs/oschome.json)` parses equal to
   today's `profiles/wayne.json` (byte-equal after the formatting-only commit), and the rendered worker
   job and workspace guide for it are unchanged.
3. **A second site in every suite**: `sites/example/` (synthetic, never deployed) differs at every
   variation point. hpcworker's tests, the extension's vitest and mock portal, the desktop edition's
   ssh lab and the engine's tests run once per bundled module. Expected values come from each module's
   `expect.json`, not from Wayne State literals in the tests.
4. **The site-literal lint**: a test collects every host, path, partition, QoS, URL and host key from
   all modules and fails on any core source line that spells one. Comments that record where something
   was measured are kept and marked, so the record survives.
5. **Texts complete**: every text key the core uses has a value for each enabled feature of each site.
6. **Live check**: the probe job compares what a module declares (egress, node temp, runtime, binds,
   host key) with what it measures, skipping what the module does not declare, and writes the result
   to the module's `facts/`; a declaration that disagrees with a measurement fails validation until a
   person resolves it.

## 6. Writing a module for a new university

1. Run `hpcworker discover` on the login node and the probe job on a compute node; they seed
   `site.json` with what they find and write what they measured, with when and where, to `facts/`.
2. Fill the rest from the university's own pages: portal, VPN, second factor, account names, policy
   (each rule with its source), the student-facing words.
3. Write the lab module for the group that will host the shared copy and images.
4. Run the conformance suite (sections 5.1 to 5.5) locally; it needs no cluster.
5. Deploy the shared copy with `deploy_shared.sh --site <site> --lab <lab>` and run the probe (5.6).
6. Rebuild the clients so they carry the new composed profile; the bridge's allow list follows.

What a new university cannot do with a module alone: use a scheduler, portal sign-in, second factor or
access-list kind the core does not implement yet. Those are core changes, reviewed like any other.

## 7. The gaps, by repository

Every gap below is a Linear issue in the project *U — University Site Modules* (team Beethoven).
Line numbers are from each repository's `main` on 2026-10-04 and will drift; the issue holds the full
list. "Owner" is who builds it; the coordinator assigns one thread per repository at a time.

### 7.1 hpcworker (the framework and the maintainer's tools)

The core is site-neutral by design (the report's twelve-site sample shaped it), so most of what is
left is a handful of literals and two structural gaps: the profile mixes three layers, and the tests
only ever load `wayne.json`.

| Issue | Gap | Where today |
|---|---|---|
| BEE-199 (U-1) | One flat profile holds site, lab and product values; no layer owns a field | `framework/profiles/wayne.json`; `lib/profile.py` `SCHEMA` (~59-115) |
| BEE-200 (U-2) | No second site; every suite and fixture loads Wayne State only | `framework/tests/`, `tests/fixtures/` |
| BEE-201 (U-3) | Nothing stops a site literal entering core code | (new test) |
| BEE-202 (U-4) | Literals in code: requeue switched on by the QoS *name* `requeue`; the probe's `/rs/*`; the refuse-list's `.beethoven*`/`.ashley*`; the Slurm binds measured on asx1; the GPU partition regex; fixed short-job sizes; "--profile wayne" in an error | `lib/profile.py:523,664,784`, `lib/profile_sh.sh:86`, `profile.awk:581`, `jobs/probe.sbatch:55`, `lib/adapters/common.sh:121,389-442`, `bin/hpcworker:313` |
| BEE-203 (U-5) | The allocation `account` is never passed (`srun` without `-A`); harmless at Wayne State, a failure where one is required | `lib/adapters/slurm.sh:115-128`, `bin/hpcworker:651` |
| BEE-204 (U-6) | Slurm options in calls meant to be neutral (`-D`, `--export=ALL,...`, `%T|%r|%S|%N`) | `bin/hpcworker:651,795-800,1172`, `jobs/worker.sbatch.tpl:274` |
| BEE-205 (U-7) | Tools default to `site=wayne host=wsu-grid`, the AccessID pattern and `reqp`/`requeue` | `tools/deploy_shared.sh:171`, `tools/grid_access.sh:77,308`, `tools/grid_ci.sbatch:6-7`, `tools/grid_access_task.ps1:53` |
| BEE-206 (U-8) | Rules live in prose and tests, without their source; the 60 s floor is written in three places | `tests/test_login_node.py:25-26`, `lib/browser_key.sh:40`, `bin/hpcworker:980,1032` |
| BEE-207 (U-9) | Measurements share the file with declarations (`egress.measured`, the host key, `ood_auth`, dates inside `notes`) | `profiles/wayne.json` |
| BEE-208 (U-10) | An account's profile is a full copy; only 16 fields follow the site afterwards | `bin/hpcworker:461-466`, `lib/profile.py:306-309`, `profile.awk:93,212-227` |
| BEE-209 (U-11) | Docs present Wayne State as *the* site ("Adding a university" says copy `wayne.json`) | `framework/README.md`, `docs/ARCHITECTURE.md` section 2, `docs/WAYNE_STATE_PILOT.md` |

### 7.2 beethoven-extension (the browser edition and its bridge)

The most Wayne-bound client after the VS Code edition: Wayne State is both the default and the only
option, and its portal, VPN and second factor are assumed in behaviour, not just in values.

| Issue | Gap | Where today |
|---|---|---|
| BEE-210 (U-12) | `DEFAULT_SITE = 'wayne'` and a guess from the portal's second DNS label choose the site | `entrypoints/background.ts:135,582,664,722-723,751,2931,3018,3156` |
| BEE-211 (U-13) | The ssh door, host-key pin and links are constants | `core/bridge.ts:30-33,138,311,316`, `background.ts:3010-3012`, `core/signin.ts` |
| BEE-212 (U-14) | Student sentences name Wayne State, AccessID, GlobalProtect, Google Authenticator | the panel, onboarding and sign-in sheet texts |
| BEE-213 (U-15) | Behaviour fits one kind each: HTTP basic portal sign-in and its start page, a TOTP prompt (`TWO_FA_REFUSAL_RE`, `CODE_PROMPT_RE`), `ACCOUNT_RE`, `useVpn('GlobalProtect')` | `background.ts:1683-1691`, `core/channel.ts:5`, `core/signin.ts` |
| BEE-214 (U-16) | The bridge's built-in allow list is `grid.wayne.edu:22`, by hand, in four implementations | `helper/src/common/bridge.py:26`, `bridge.pl:35`, `rust/src/main.rs:31`, `windows/bridge.ps1:30` |
| BEE-215 (U-17) | The mock portal, the ssh stand-in and the fixtures model Wayne State only | `mock-ood/server.mjs:79,153-175`, `mock-ood/lib/*.mjs`, `test/sshgrid/server.py` |

### 7.3 beethoven-desktop

Already mostly neutral (titles and the VPN message come from the profile).

| Issue | Gap | Where today |
|---|---|---|
| BEE-216 (U-18) | Default site `wayne` in the config and both manifests; `hmac-sha1` and `inet` hard-coded as ssh options; Wayne State words in tests | `src/config.ts:33`, `bundle/manifest.json:21,56-61`, `plugin/.claude-plugin/plugin.json:17,31-35`, `src/ssh.ts:101-102`, `src/grid.ts:164` |

### 7.4 beethoven-vscode

Reads no site profile at all; its grid side moves onto hpcworker under the base design
(`/mnt/project-files/base/DESIGN.md` section 7), which removes most of it.

| Issue | Gap | Where today |
|---|---|---|
| BEE-217 (U-19) | warrior, `wsu-grid`, `nas.grid.wayne.edu`, AccessID and `@wayne.edu` identity, the GPU partition `galhp` with QoS `gpu`, the wizard, about 51 lines of "Wayne State"; the diagnostics scrubber recognises only Wayne State's shapes of personal data | `extension/src/`, `grid/` |

The VS Code test file `diagReport.test.ts` carries what look like real identifiers; the coordinator
has passed that to the desktop thread, which owns the open VS Code change.

### 7.5 beethoven-base

| Issue | Gap | Where today |
|---|---|---|
| BEE-218 (U-20) | No shared client reader for modules: matching, text lookup with fallback, layered fields | the base design already moves `profile.ts` there |

### 7.6 The engine (beethoven-agents, beethoven-qa, beethoven-research)

| Issue | Gap | Where today |
|---|---|---|
| BEE-219 (U-21) | bee's image path, runtime module and node temp are Wayne State's literals; the image build's scratch and output; guard tests use Wayne inputs; the runbook's commands work only there | `src/beethoven_agents/bee/bee-grid.sh:49,53-56,59-63`, `containers/build.sh:42,48`, `tests/test_guard.py`, `docs/` |
| BEE-220 (U-22) | Docs call CentOS 7 and Python 3.6 "the grid's" floors | beethoven-qa `plugin/skills/improve-existing-module/SKILL.md:28,33`, `docs/CONSUMING.md:26`, `ci.yml:3` |

beethoven-research's code holds no Wayne State literal; its `CLAUDE.md` and `ci.yml:3` describe the
grid in prose, which is accurate and stays.

### 7.7 Decisions (no code until answered; defaults below)

BEE-221 (U-23) where modules live; BEE-222 (U-24) whether the agreement, the privacy statement and the
store texts stop naming Wayne State now or when a second site is approved. Section 9.

## 8. Order of work and owners

The boundary is proven before anything moves across it. Phase A builds the module format and its
checks with no change of behaviour; phase B empties the framework of Wayne State; phase C does the
clients, which can only read modules once the framework composes them.

| Phase | Issues | What "done" means | Owner (assigned by the coordinator, 2026-10-05 00:08Z) |
|---|---|---|---|
| A | BEE-199, BEE-200, BEE-201 (hpcworker) | the composed Wayne State profile parses equal to today's `wayne.json`, then is byte-equal after a formatting-only commit; the example site passes every framework test; the lint is green | the site-module thread, on top of the desktop thread's framework 18 (`worker_race`) |
| A | BEE-219 (beethoven-agents) | the engine reads the vendored composed profile; the gate proves the reader; no Wayne literal in code | the site-module thread, now |
| B | BEE-202, BEE-203, BEE-206, BEE-207, BEE-208, BEE-204, BEE-205, BEE-209 (hpcworker) | each issue's test fails before and passes after; both sites green | the site-module thread, after phase A |
| C | BEE-218 (beethoven-base) | one reader the three clients share | after base PR #1 and greg's base decisions |
| C | BEE-210 to BEE-215, BEE-214 (beethoven-extension) | the extension runs its suites against both sites; the bridge's list is generated | after the extension's 15.0.0 PR merges; ask the coordinator first |
| C | BEE-216 (beethoven-desktop) | no default site; ssh options from the module | when nothing else is open there; ask the coordinator first |
| C | BEE-217 (beethoven-vscode) | reads the module after its move onto hpcworker | after the account-setting PR and the base move |
| C | BEE-220 (beethoven-qa) | docs reworded | after the code-quality thread's open PRs merge |

The order inside phase B puts the account bug (BEE-203) and the requeue flag (part of BEE-202) first,
since each is a wrong behaviour at a second site, not only a literal.

The desktop thread's all-queue launch (`worker_race`) is the first role list (section 2.2's "lab's
choice of partition for long workers"): it lands as a lab-owned field and needs no change for this
design.

## 9. Decisions for greg

Neither blocks any work; each has a default the build follows until greg says otherwise.

1. **Where modules live (BEE-221). Decided by greg, 2026-10-05 00:59Z: a repository of their own,
   `OpenSpineConsortium/beethoven-sites`.** greg creates it by hand. It holds the modules and their
   records; hpcworker keeps the schema, the owner table, the composer and the composed profiles, and
   carries a pinned copy of the modules under `framework/sites/` with an ORIGIN record and a pull
   script, as beethoven-agents carries `profiles/`. hpcworker also publishes the module schema as
   data, which beethoven-sites pins and checks modules against with a standard-library checker, so
   a module's author never needs hpcworker's code. The recommendation it overrode follows, kept as
   the record. Default: in hpcworker, `framework/sites/<site>/`, beside the
   profiles they compose into. The browser and desktop editions already take `framework/profiles/` as
   data and the engine will (BEE-219), which crosses no dependence line, and there is no new repository, ruleset or secret to set up. A
   repository of their own (`beethoven-sites`) becomes worth it when someone outside the project
   writes a module, such as a lab lead at another university who should not see the framework's
   code, or when modules change on a different rhythm from the framework; the move is then a
   `git mv` and one path in each `pull.sh`. This settles the earlier idea of a fourth repository for
   the grid's rules (`plan/REPO_SPLIT.md` section 2) in favour of a folder, for now.
2. **The legal and store texts (BEE-222). Decided by greg, 2026-10-05 00:33Z: when a second site
   is approved.** They keep naming Wayne State, GlobalProtect,
   Google Authenticator and AccessIDs until a second site is approved. They are accurate today,
   since the private listing serves approved Wayne State students only, and changing them is a new
   terms version that every student accepts again. The alternative is neutral wording now ("your
   university's VPN", "your account name") with Wayne State as the named pilot. The venue clause
   (Wayne County, Michigan) is the vendor's and stays either way.

## 10. Not yet measured

- Whether any second university's portal, VPN or second factor fits the closed lists above; the
  example module is synthetic, and the report's twelve-site sample is documentation, not a deployment.
- Whether Duo or a "Passcode or option" prompt reaches the extension's sign-in sheet in a form the
  sitting can classify (today it would be classed "other").
- Whether `sacct`'s held-job behaviour holds at Wayne State (`slurm.sh:149` says so itself).
- Whether a site without POSIX ACLs (GPFS or NFSv4 ACLs) can keep the approved-list model.
