# MGDC Security Dashboard — Power BI (PBIP)

Comprehensive SharePoint security dashboard built on Microsoft Graph Data Connect (MGDC) datasets. Opens directly in Power BI Desktop as a PBIP project.

## Data Sources

Five MGDC SharePoint datasets from a Microsoft Fabric Lakehouse (via SQL analytics endpoint):

| Dataset | Table | Source Cols | Calc Cols | Description |
|---------|-------|------------|-----------|-------------|
| SharePoint_Sites_v1 | SharePointSites | 22 | 11 | Site inventory & risk scoring |
| SharePoint_Files_v1 | SharePointFiles | 18 | 10 | File metadata & protection status |
| SharePoint_FileActions_v1 | SharePointFileActions | 13 | 10 | User activity & anomaly detection |
| SharePoint_Permissions_v1 | SharePointPermissions | 14 | 11 | Permission risk classification |
| SharePoint_Groups_v1 | SharePointGroups | 12 | 5 | Group membership & risk levels |

Plus a calculated **DimDate** dimension (2020-2026) and a **_Measures** table with 120 DAX measures.

## Data Model

Star schema with SharePointSites as the hub. 8 relationships:

- Files → Sites (SiteId)
- FileActions → Sites (SiteId), Files (FileId), DimDate (ActionDate)
- Permissions → Sites (SiteId), Files (FileId), DimDate (CreatedDateTime, inactive)
- Groups → Sites (SiteId)

## Report Pages (10)

| # | Page | Visuals | Focus |
|---|------|---------|-------|
| 1 | Executive Security Overview | 10 | KPIs, health score gauge, risk breakdown |
| 2 | External Sharing Exposure | 10 | Anonymous links, org links, oversharing |
| 3 | Permission Deep Dive | 8 | Risk distribution, role analysis, inheritance |
| 4 | Sensitivity & Encryption | 8 | Label coverage, protection gaps |
| 5 | User Activity & Anomalies | 11 | After-hours, suspicious, external downloads |
| 6 | Site Security Posture | 8 | Device policies, orphaned, conditional access |
| 7 | Group & Membership Risks | 8 | Ownerless, overlarge, external members |
| 8 | File Intelligence & Storage | 8 | Version bloat, reclaimable storage |
| 9 | Stale Content & Zombie Permissions | 8 | Abandoned sites, ancient permissions |
| 10 | Risk Scoring & Recommendations | 8 | Composite index (weighted 5 components) |

**Total: 87 visuals**, 120 DAX measures across 10 display folders.

## 120 DAX Measures

Organized in display folders:

1. **Executive Overview** (12) — Total Sites/Files/Storage, Security Score/Grade, Critical Sites
2. **External Sharing** (14) — Anonymous/Org/External links, Never-Expiring, Oversharing Risk
3. **Permission Analysis** (14) — Critical/High Risk, Overprivileged, Sprawl Index
4. **Sensitivity & Encryption** (12) — Label Coverage %, Encrypted %, Unprotected %
5. **User Activity** (16) — Downloads/Deletes, After-Hours %, Suspicious, External
6. **Site Security** (10) — No Device Policy, Orphaned, Locked, Missing CA
7. **Group Risks** (11) — External Members, Ownerless, Overlarge
8. **File Intelligence** (11) — Version Storage, Bloat Ratio, Reclaimable
9. **Stale Access** (10) — Stale Files/Sites >180d, Zombie Links >1yr
10. **Risk Scoring** (10) — Composite Index (Sharing 35% + Perms 25% + Labels 20% + Stale 10% + Groups 10%)

## Setup

### Fabric Deployment (DirectLake)

1. Connect this repo to a Fabric workspace via **Git Integration**
2. The semantic model uses **DirectLake** mode — reads Delta tables directly from your Lakehouse
3. After syncing, bind the semantic model to your Lakehouse:
   - Open the semantic model in Fabric → **Settings → Gateway and cloud connections**
   - Map the connection to your Lakehouse containing the MGDC tables
4. No refresh needed — DirectLake reads Delta tables on demand

### Expected Lakehouse tables

The following Delta tables must exist in your Lakehouse (Tables section):

```
dbo.SharePoint_Sites_v1
dbo.SharePoint_Files_v1
dbo.SharePoint_FileActions_v1
dbo.SharePoint_Permissions_v1
dbo.SharePoint_Groups_v1
```

## Project Structure

```
MGDCSecurityDashboard.pbip                    # Project file
MGDCSecurityDashboard.SemanticModel/          # Data model
  definition.pbism
  .platform
  definition/
    database.tmdl
    model.tmdl                                # 8 relationships, 7 table refs
    expressions.tmdl                          # Fabric Lakehouse parameters
    tables/
      SharePointSites.tmdl                    # 22+11 columns, M query
      SharePointFiles.tmdl                    # 18+10 columns, M query
      SharePointFileActions.tmdl              # 13+10 columns, M query
      SharePointPermissions.tmdl              # 14+11 columns, M query
      SharePointGroups.tmdl                   # 12+5 columns, M query
      DimDate.tmdl                            # Calculated table (2020-2026)
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
- No conditional access: +10

**Composite Risk Index (weighted):**
- Sharing Risk: 35%
- Permission Risk: 25%
- Label Coverage Gap: 20%
- Stale Content: 10%
- Group Risk: 10%
