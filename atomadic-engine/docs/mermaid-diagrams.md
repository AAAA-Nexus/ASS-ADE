# Generated Mermaid Diagrams

Generated from local control JSON ledgers and `capabilities/registry.json`.

## JSON Lifecycle

```mermaid
flowchart LR
  refresh["refresh --collect-pytest --docs"]
  inventory["inventory/latest.json"]
  outputs["ASS_ADE_OUTPUT.json files"]
  stress["outputs/stress/*.json"]
  registry["capabilities/registry.json"]
  index["CONTROL_INDEX.json"]
  matrix["docs/capability-matrix.md"]
  status["docs/local-control-status.md"]
  diagrams["docs/diagrams/*.mmd"]
  refresh --> inventory
  refresh --> stress
  refresh --> registry
  inventory --> index
  outputs --> index
  stress --> index
  registry --> index
  registry --> matrix
  index --> status
  index --> diagrams
  registry --> diagrams
```

## Local Control

```mermaid
flowchart TD
  parent["C:/!aaaa-nexus"]
  control["!ass-ade-control"]
  inventory["inventory/latest.json"]
  index["CONTROL_INDEX.json"]
  stress["outputs/stress"]
  docs["generated docs"]
  parent --> control
  control --> inventory
  control --> index
  control --> stress
  index --> docs

  subgraph Local_Siblings[Local siblings]
    sibling_0["!ass-ade<br/>mixed-source-dump<br/>unstamped"]
    sibling_1["!ass-ade-dev<br/>rebuild-output<br/>stamped"]
    sibling_2["!ass-ade-legacy<br/>git-working-copy-dirty<br/>unstamped"]
    sibling_3["!ass-ade-merged<br/>rebuild-output<br/>stamped"]
    sibling_4["!ass-ade-rebuilt-test<br/>rebuild-output<br/>stamped"]
    sibling_5["ass-ade-fix<br/>git-working-copy-dirty<br/>unstamped"]
    sibling_6["ass-ade-github-latest<br/>canonical-mirror<br/>unstamped"]
    sibling_7["ass-ade-unified<br/>rebuild-output<br/>stamped"]
  end
  parent --> sibling_0
  sibling_1 --> index
  parent --> sibling_2
  sibling_3 --> index
  sibling_4 --> index
  parent --> sibling_5
  sibling_6 --> stress
  sibling_7 --> index
```

## Capability Status

```mermaid
flowchart TD
  registry["capabilities/registry.json\n34 total"]

  subgraph Overall[Overall status]
    ov_complete["OK complete: 26"]
    ov_partial["~ partial: 3"]
    ov_missing["GAP missing: 5"]
  end
  registry --> Overall

  subgraph Areas[By area]
    area_a2a["A2A [C:1 M:1]"]
    area_agent["Agent [C:2 M:2]"]
    area_blueprint["Blueprint [C:2]"]
    area_certification["Certification [C:1]"]
    area_context["Context [C:1]"]
    area_core["Core [C:4]"]
    area_docs["Docs [C:1]"]
    area_evolution["Evolution [C:1]"]
    area_ide["IDE [M:1]"]
    area_mcp["MCP [C:1 P:1]"]
    area_nexus["Nexus [C:3]"]
    area_payment["Payment [P:1 M:1]"]
    area_provider["Provider [C:1]"]
    area_quality["Quality [C:2]"]
    area_rebuild["Rebuild [C:4]"]
    area_workflow["Workflow [C:2 P:1]"]
  end
  registry --> Areas
```

Standalone Mermaid files are written under `docs/diagrams/`.
