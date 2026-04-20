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
flowchart LR
  registry["capabilities/registry.json"]
  docs["docs/capability-matrix.md"]
  registry --> docs

  subgraph Status[Capability status]
    status_complete["complete: 26"]
    registry --> status_complete
    status_partial["partial: 3"]
    registry --> status_partial
    status_missing["missing: 5"]
    registry --> status_missing
  end

  subgraph Areas[Capability areas]
    area_a2a["a2a: 2"]
    registry --> area_a2a
    area_agent["agent: 4"]
    registry --> area_agent
    area_blueprint["blueprint: 2"]
    registry --> area_blueprint
    area_certification["certification: 1"]
    registry --> area_certification
    area_context["context: 1"]
    registry --> area_context
    area_core["core: 4"]
    registry --> area_core
    area_docs["docs: 1"]
    registry --> area_docs
    area_evolution["evolution: 1"]
    registry --> area_evolution
    area_ide["ide: 1"]
    registry --> area_ide
    area_mcp["mcp: 2"]
    registry --> area_mcp
    area_nexus["nexus: 3"]
    registry --> area_nexus
    area_payment["payment: 2"]
    registry --> area_payment
    area_provider["provider: 1"]
    registry --> area_provider
    area_quality["quality: 2"]
    registry --> area_quality
    area_rebuild["rebuild: 4"]
    registry --> area_rebuild
    area_workflow["workflow: 3"]
    registry --> area_workflow
  end
```

Standalone Mermaid files are written under `docs/diagrams/`.
