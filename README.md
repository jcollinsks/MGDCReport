# MGDC Security Dashboard — Power BI (PBIP)

Comprehensive SharePoint security dashboard built on Microsoft Graph Data Connect (MGDC) datasets. Opens directly in Power BI Desktop as a PBIP project.

## Data Sources

Five MGDC SharePoint tables via DirectQuery to Analysis Services (the MGDC semantic model in Fabric):

| Dataset | Table | Source Cols | Calc Cols | Description |
|---------|-------|------------|-----------|-------------|
| SharePoint_Sites_v1 | SPOSites | 25 | 11 | Site inventory & risk scoring |
| SharePoint_Files_v1 | SPOFiles | 22 | 10 | File metadata & protection status |
| SharePoint_FileActions_v1 | SPOFileActions | 17 | 10 | User activity & anomaly detection |
| SharePoint_Permissions_v1 | SPOPermissions | 21 | 11 | Permission risk classification |
| SharePoint_Groups_v1 | SPOGroups | 9 | 2 | Group membership & risk levels |

Plus a **_Measures** table with 120 DAX measures across 10 display folders.

## Data Model

Star schema with SPOSites (PK: `Id`) as the hub. 6 relationships:

- SPOFiles → SPOSites (SiteId → Id)
- SPOFileActions → SPOSites (SiteId → Id), SPOFiles (ListItemId → ItemId)
- SPOPermissions → SPOSites (SiteId → Id), SPOFiles (ListItemId → ItemId)
- SPOGroups → SPOSites (SiteId → Id)

## Report Pages (10)

| # | Page | Visuals | Focus |
|---|------|---------|-------|
| 1 | Executive Security Overview | 10 | KPIs, health score gauge, risk breakdown |
| 2 | External Sharing Exposure | 10 | Anonymous links, org links, oversharing |
| 3 | Permission Deep Dive | 8 | Risk distribution, role analysis, link types |
| 4 | Sensitivity & Encryption | 8 | Label coverage, protection gaps |
| 5 | User Activity & Anomalies | 11 | After-hours, suspicious, external downloads |
| 6 | Site Security Posture | 8 | Device policies, orphaned, read-locked |
| 7 | Group & Membership Risks | 8 | Ownerless, group types, risk levels |
| 8 | File Intelligence & Storage | 8 | Version bloat, reclaimable storage |
| 9 | Stale Content & Zombie Permissions | 8 | Abandoned sites, ancient permissions |
| 10 | Risk Scoring & Recommendations | 8 | Composite index (weighted 5 components) |

**Total: 87 visuals**, 120 DAX measures across 10 display folders.

## 120 DAX Measures

Organized in display folders:

1. **Executive Overview** (12) — Total Sites/Files/Storage, Security Score/Grade, Critical Sites
2. **External Sharing** (14) — Anonymous/Org/External links, Never-Expiring, External Link Users
3. **Permission Analysis** (14) — Critical/High Risk, Overprivileged, Total Shared Users, Sprawl Index
4. **Sensitivity & Encryption** (12) — Label Coverage %, Encrypted %, Unprotected %
5. **User Activity** (16) — Downloads/Deletes, After-Hours %, Suspicious, External
6. **Site Security** (10) — No Device Policy, Orphaned, Read-Locked, Teams Connected Sites
7. **Group Risks** (11) — Security/M365/SharePoint Groups, Ownerless, Critical Risk Groups
8. **File Intelligence** (11) — Version Storage, Bloat Ratio, Reclaimable
9. **Stale Access** (10) — Stale Files/Sites >180d, Zombie Links >1yr
10. **Risk Scoring** (10) — Composite Index (Sharing 35% + Perms 25% + Labels 20% + Stale 10% + Groups 10%)

## Setup

1. Open `MGDCSecurityDashboard.pbip` in Power BI Desktop
2. The semantic model connects via DirectQuery to the **MGDC** semantic model in the **workforce** workspace
3. Update the connection in `expressions.tmdl` if your workspace or model name differs:
   ```
   AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/<workspace>", "<model>")
   ```
4. Calculated columns, measures, and relationships are applied on top of the remote model

### Required remote model tables

The following tables must exist in your MGDC semantic model:

```
SPOSites
SPOFiles
SPOFileActions
SPOPermissions
SPOGroups
```

## Project Structure

```
MGDCSecurityDashboard.pbip                    # Project file
MGDCSecurityDashboard.SemanticModel/          # Data model
  definition.pbism
  .platform
  definition/
    database.tmdl
    model.tmdl                                # 6 relationships, 6 table refs
    expressions.tmdl                          # DirectQuery to AS connection
    tables/
      SPOSites.tmdl                           # 25+11 columns
      SPOFiles.tmdl                           # 22+10 columns
      SPOFileActions.tmdl                     # 17+10 columns
      SPOPermissions.tmdl                     # 21+11 columns
      SPOGroups.tmdl                          # 9+2 columns
      _Measures.tmdl                          # 120 DAX measures
MGDCSecurityDashboard.Report/                 # Report visuals
  definition.pbir
  .platform
  definition/
    report.json
    version.json
    pages/                                    # 10 pages, 87 visuals
```

## Risk Scoring Methodology

**Site Risk Score (0-100):**
- External sharing enabled: +25
- No sensitivity label: +20
- No device access policy: +15
- Orphaned (no owner): +15
- Stale (>180 days): +15
- Read-locked: +10

**Composite Risk Index (weighted):**
- Sharing Risk: 35%
- Permission Risk: 25%
- Label Coverage Gap: 20%
- Stale Content: 10%
- Group Risk: 10%
