-- ============================================================
-- MGDC Test Database — Seed Data
-- Realistic sample data exercising all risk-scoring paths
-- ============================================================

SET NOCOUNT ON;

-- ============================================================
-- Helper: Snapshot date = today
-- ============================================================
DECLARE @Snap DATETIME2 = CAST(GETDATE() AS DATE);
DECLARE @Now  DATETIME2 = GETDATE();

-- ============================================================
-- 1. SPOSites — 50 sites
-- Mix: Team / Communication / Personal (OneDrive)
-- Variance: external sharing, orphaned, stale, read-locked,
--           labeled/unlabeled, device-blocked, hub sites
-- ============================================================

-- Site GUIDs (reused across tables for referential consistency)
-- Sites 01-20: Team sites
-- Sites 21-35: Communication sites
-- Sites 36-50: OneDrive / Personal sites

INSERT INTO dbo.SPOSites (
    Id, Url, [RootWeb.Title], [RootWeb.WebTemplate],
    CreatedTime, LastContentChange, StorageUsed, StorageQuota,
    IsInRecycleBin, [SensitivityLabelInfo.Id], [SensitivityLabelInfo.DisplayName],
    IsExternalSharingEnabled, [Owner.Email], [Owner.Name],
    GroupId, IsTeamsConnectedSite, ReadLocked, HubSiteId,
    BlockAccessFromUnmanagedDevices, GeoLocation, SnapshotDate,
    LastSecurityModifiedDate, IsCommunicationSite, IsOneDrive, Privacy
) VALUES
-- === TEAM SITES (01-20) ===
-- 01: Low risk — labeled, internal-only, active, owned, device-blocked
('site-guid-0001', 'https://contoso.sharepoint.com/sites/Engineering',
 'Engineering', 'Group#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-5,@Now),
 5368709120, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'alice@contoso.com', 'Alice Johnson', 'grp-001', 1, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 0, 0, 'Private'),

-- 02: Medium risk — external sharing on, no device policy
('site-guid-0002', 'https://contoso.sharepoint.com/sites/Marketing',
 'Marketing', 'Group#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-15,@Now),
 10737418240, 27917287424, 0,
 'label-gen-001', 'General', 1,
 'bob@contoso.com', 'Bob Smith', 'grp-002', 1, 0, 'hub-001',
 0, 'NAM', @Snap, DATEADD(DAY,-20,@Now), 0, 0, 'Public'),

-- 03: High risk — external sharing, no label, no device policy, orphaned
('site-guid-0003', 'https://contoso.sharepoint.com/sites/Sales-External',
 'Sales External Collab', 'Group#0', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-200,@Now),
 2147483648, 27917287424, 0,
 NULL, NULL, 1,
 NULL, NULL, 'grp-003', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-250,@Now), 0, 0, 'Public'),

-- 04: Critical risk — external sharing, no label, no device policy, orphaned, stale, read-locked
('site-guid-0004', 'https://contoso.sharepoint.com/sites/Legacy-Project',
 'Legacy Project Alpha', 'Group#0', DATEADD(YEAR,-4,@Now), DATEADD(DAY,-400,@Now),
 1073741824, 27917287424, 0,
 NULL, NULL, 1,
 NULL, NULL, 'grp-004', 0, 1, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-500,@Now), 0, 0, 'Private'),

-- 05: Low risk — labeled, internal, active, owned
('site-guid-0005', 'https://contoso.sharepoint.com/sites/HR',
 'Human Resources', 'Group#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-2,@Now),
 8589934592, 27917287424, 0,
 'label-hbi-001', 'Highly Confidential', 0,
 'carol@contoso.com', 'Carol White', 'grp-005', 1, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-5,@Now), 0, 0, 'Private'),

-- 06: Medium risk — external sharing, labeled
('site-guid-0006', 'https://contoso.sharepoint.com/sites/Finance',
 'Finance', 'Group#0', DATEADD(MONTH,-18,@Now), DATEADD(DAY,-30,@Now),
 16106127360, 27917287424, 0,
 'label-conf-001', 'Confidential', 1,
 'dave@contoso.com', 'Dave Brown', 'grp-006', 1, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-35,@Now), 0, 0, 'Private'),

-- 07: Low risk, recently created
('site-guid-0007', 'https://contoso.sharepoint.com/sites/NewProject',
 'New Project Beta', 'Group#0', DATEADD(DAY,-45,@Now), DATEADD(DAY,-1,@Now),
 536870912, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'eve@contoso.com', 'Eve Davis', 'grp-007', 1, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-2,@Now), 0, 0, 'Private'),

-- 08: High risk — no label, orphaned, external sharing
('site-guid-0008', 'https://contoso.sharepoint.com/sites/Contractors',
 'Contractors Portal', 'Group#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-100,@Now),
 3221225472, 27917287424, 0,
 NULL, NULL, 1,
 NULL, NULL, 'grp-008', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-120,@Now), 0, 0, 'Public'),

-- 09: Recycled site
('site-guid-0009', 'https://contoso.sharepoint.com/sites/OldTeam',
 'Old Team Site', 'Group#0', DATEADD(YEAR,-5,@Now), DATEADD(YEAR,-1,@Now),
 0, 27917287424, 1,
 NULL, NULL, 0,
 'frank@contoso.com', 'Frank Wilson', 'grp-009', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(YEAR,-1,@Now), 0, 0, 'Private'),

-- 10: Overprovisioned site — huge quota, tiny usage
('site-guid-0010', 'https://contoso.sharepoint.com/sites/Archive',
 'Archive', 'Group#0', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-90,@Now),
 10485760, 10737418240, 0,
 'label-gen-001', 'General', 0,
 'grace@contoso.com', 'Grace Lee', 'grp-010', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-95,@Now), 0, 0, 'Private'),

-- 11-15: More team sites with varying risk profiles
('site-guid-0011', 'https://contoso.sharepoint.com/sites/Legal',
 'Legal', 'Group#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-7,@Now),
 12884901888, 27917287424, 0,
 'label-hbi-001', 'Highly Confidential', 0,
 'henry@contoso.com', 'Henry Taylor', 'grp-011', 1, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 0, 0, 'Private'),

('site-guid-0012', 'https://contoso.sharepoint.com/sites/IT-Operations',
 'IT Operations', 'Group#0', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-3,@Now),
 7516192768, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'irene@contoso.com', 'Irene Martin', 'grp-012', 1, 0, 'hub-002',
 1, 'NAM', @Snap, DATEADD(DAY,-5,@Now), 0, 0, 'Private'),

('site-guid-0013', 'https://contoso.sharepoint.com/sites/R-and-D',
 'Research & Development', 'Group#0', DATEADD(MONTH,-8,@Now), DATEADD(DAY,-12,@Now),
 4294967296, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'jack@contoso.com', 'Jack Anderson', 'grp-013', 1, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-15,@Now), 0, 0, 'Private'),

('site-guid-0014', 'https://contoso.sharepoint.com/sites/Vendor-Collab',
 'Vendor Collaboration', 'Group#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-60,@Now),
 2684354560, 27917287424, 0,
 NULL, NULL, 1,
 'karen@contoso.com', 'Karen Thomas', 'grp-014', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-70,@Now), 0, 0, 'Public'),

('site-guid-0015', 'https://contoso.sharepoint.com/sites/Executive',
 'Executive Leadership', 'Group#0', DATEADD(YEAR,-4,@Now), DATEADD(DAY,-1,@Now),
 6442450944, 27917287424, 0,
 'label-hbi-001', 'Highly Confidential', 0,
 'larry@contoso.com', 'Larry Jackson', 'grp-015', 1, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-2,@Now), 0, 0, 'Private'),

-- 16-20: Edge cases
('site-guid-0016', 'https://contoso.sharepoint.com/sites/Training',
 'Training Portal', 'Group#0', DATEADD(MONTH,-6,@Now), DATEADD(DAY,-45,@Now),
 1610612736, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'mary@contoso.com', 'Mary Harris', 'grp-016', 0, 0, 'hub-002',
 0, 'NAM', @Snap, DATEADD(DAY,-50,@Now), 0, 0, 'Public'),

('site-guid-0017', 'https://contoso.sharepoint.com/sites/CustomerSupport',
 'Customer Support', 'Group#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-8,@Now),
 4831838208, 27917287424, 0,
 'label-gen-001', 'General', 1,
 'nancy@contoso.com', 'Nancy Clark', 'grp-017', 1, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 0, 0, 'Private'),

-- Stale team site, owned but no label
('site-guid-0018', 'https://contoso.sharepoint.com/sites/ProjectGamma',
 'Project Gamma', 'Group#0', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-250,@Now),
 858993459, 27917287424, 0,
 NULL, NULL, 0,
 'oscar@contoso.com', 'Oscar Wright', 'grp-018', 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-260,@Now), 0, 0, 'Private'),

-- Teams-connected, EUR geo
('site-guid-0019', 'https://contoso.sharepoint.com/sites/EMEA-Team',
 'EMEA Team', 'Group#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-4,@Now),
 3758096384, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'peter@contoso.com', 'Peter Adams', 'grp-019', 1, 0, NULL,
 1, 'EUR', @Snap, DATEADD(DAY,-6,@Now), 0, 0, 'Private'),

('site-guid-0020', 'https://contoso.sharepoint.com/sites/APAC-Sales',
 'APAC Sales', 'Group#0', DATEADD(MONTH,-10,@Now), DATEADD(DAY,-20,@Now),
 2147483648, 27917287424, 0,
 'label-gen-001', 'General', 1,
 'quinn@contoso.com', 'Quinn Baker', 'grp-020', 1, 0, NULL,
 0, 'APC', @Snap, DATEADD(DAY,-25,@Now), 0, 0, 'Public'),

-- === COMMUNICATION SITES (21-35) ===
('site-guid-0021', 'https://contoso.sharepoint.com/sites/Intranet',
 'Contoso Intranet', 'SitePage#0', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-1,@Now),
 21474836480, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'alice@contoso.com', 'Alice Johnson', NULL, 0, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-3,@Now), 1, 0, NULL),

('site-guid-0022', 'https://contoso.sharepoint.com/sites/CompanyNews',
 'Company News', 'SitePage#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-2,@Now),
 5368709120, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'bob@contoso.com', 'Bob Smith', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-5,@Now), 1, 0, NULL),

('site-guid-0023', 'https://contoso.sharepoint.com/sites/Benefits',
 'Employee Benefits', 'SitePage#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-30,@Now),
 1073741824, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'carol@contoso.com', 'Carol White', NULL, 0, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-35,@Now), 1, 0, NULL),

('site-guid-0024', 'https://contoso.sharepoint.com/sites/Events',
 'Company Events', 'SitePage#0', DATEADD(MONTH,-6,@Now), DATEADD(DAY,-10,@Now),
 536870912, 27917287424, 0,
 NULL, NULL, 1,
 'dave@contoso.com', 'Dave Brown', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-15,@Now), 1, 0, NULL),

-- Orphaned communication site, stale
('site-guid-0025', 'https://contoso.sharepoint.com/sites/OldCampaign',
 'Q3 Campaign 2024', 'SitePage#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-300,@Now),
 2147483648, 27917287424, 0,
 NULL, NULL, 1,
 NULL, NULL, NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-310,@Now), 1, 0, NULL),

('site-guid-0026', 'https://contoso.sharepoint.com/sites/Policies',
 'Corporate Policies', 'SitePage#0', DATEADD(YEAR,-4,@Now), DATEADD(DAY,-15,@Now),
 3221225472, 27917287424, 0,
 'label-hbi-001', 'Highly Confidential', 0,
 'eve@contoso.com', 'Eve Davis', NULL, 0, 0, 'hub-001',
 1, 'NAM', @Snap, DATEADD(DAY,-20,@Now), 1, 0, NULL),

('site-guid-0027', 'https://contoso.sharepoint.com/sites/Brand',
 'Brand Center', 'SitePage#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-5,@Now),
 8589934592, 27917287424, 0,
 'label-gen-001', 'General', 1,
 'frank@contoso.com', 'Frank Wilson', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-8,@Now), 1, 0, NULL),

('site-guid-0028', 'https://contoso.sharepoint.com/sites/Crisis-Comms',
 'Crisis Communications', 'SitePage#0', DATEADD(MONTH,-3,@Now), DATEADD(DAY,-60,@Now),
 214748364, 27917287424, 0,
 'label-hbi-001', 'Highly Confidential', 0,
 'grace@contoso.com', 'Grace Lee', NULL, 0, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-65,@Now), 1, 0, NULL),

('site-guid-0029', 'https://contoso.sharepoint.com/sites/Sustainability',
 'Sustainability Report', 'SitePage#0', DATEADD(DAY,-60,@Now), DATEADD(DAY,-3,@Now),
 1073741824, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'henry@contoso.com', 'Henry Taylor', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-5,@Now), 1, 0, NULL),

('site-guid-0030', 'https://contoso.sharepoint.com/sites/DEI',
 'Diversity & Inclusion', 'SitePage#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-20,@Now),
 2147483648, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'irene@contoso.com', 'Irene Martin', NULL, 0, 0, 'hub-002',
 0, 'NAM', @Snap, DATEADD(DAY,-25,@Now), 1, 0, NULL),

-- More comm sites
('site-guid-0031', 'https://contoso.sharepoint.com/sites/Innovation',
 'Innovation Hub', 'SitePage#0', DATEADD(MONTH,-4,@Now), DATEADD(DAY,-7,@Now),
 4294967296, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'jack@contoso.com', 'Jack Anderson', NULL, 0, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 1, 0, NULL),

('site-guid-0032', 'https://contoso.sharepoint.com/sites/Safety',
 'Workplace Safety', 'SitePage#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-40,@Now),
 858993459, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'karen@contoso.com', 'Karen Thomas', NULL, 0, 0, 'hub-002',
 0, 'NAM', @Snap, DATEADD(DAY,-45,@Now), 1, 0, NULL),

-- Orphaned + external sharing comm site
('site-guid-0033', 'https://contoso.sharepoint.com/sites/PartnerPortal',
 'Partner Portal', 'SitePage#0', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-150,@Now),
 6442450944, 27917287424, 0,
 NULL, NULL, 1,
 NULL, NULL, NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-160,@Now), 1, 0, NULL),

('site-guid-0034', 'https://contoso.sharepoint.com/sites/ProductLaunch',
 'Product Launch 2026', 'SitePage#0', DATEADD(DAY,-30,@Now), DATEADD(DAY,-1,@Now),
 1610612736, 27917287424, 0,
 'label-conf-001', 'Confidential', 0,
 'larry@contoso.com', 'Larry Jackson', NULL, 0, 0, NULL,
 1, 'NAM', @Snap, DATEADD(DAY,-2,@Now), 1, 0, NULL),

('site-guid-0035', 'https://contoso.sharepoint.com/sites/Wellness',
 'Employee Wellness', 'SitePage#0', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-25,@Now),
 536870912, 27917287424, 0,
 'label-gen-001', 'General', 0,
 'mary@contoso.com', 'Mary Harris', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-30,@Now), 1, 0, NULL),

-- === ONEDRIVE / PERSONAL SITES (36-50) ===
('site-guid-0036', 'https://contoso-my.sharepoint.com/personal/alice_contoso_com',
 'Alice Johnson', 'SPSPERS#10', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-1,@Now),
 10737418240, 1099511627776, 0,
 NULL, NULL, 0,
 'alice@contoso.com', 'Alice Johnson', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-3,@Now), 0, 1, NULL),

('site-guid-0037', 'https://contoso-my.sharepoint.com/personal/bob_contoso_com',
 'Bob Smith', 'SPSPERS#10', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-3,@Now),
 21474836480, 1099511627776, 0,
 NULL, NULL, 1,
 'bob@contoso.com', 'Bob Smith', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-5,@Now), 0, 1, NULL),

('site-guid-0038', 'https://contoso-my.sharepoint.com/personal/carol_contoso_com',
 'Carol White', 'SPSPERS#10', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-2,@Now),
 5368709120, 1099511627776, 0,
 'label-gen-001', 'General', 0,
 'carol@contoso.com', 'Carol White', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-4,@Now), 0, 1, NULL),

('site-guid-0039', 'https://contoso-my.sharepoint.com/personal/dave_contoso_com',
 'Dave Brown', 'SPSPERS#10', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-90,@Now),
 1073741824, 1099511627776, 0,
 NULL, NULL, 0,
 'dave@contoso.com', 'Dave Brown', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-95,@Now), 0, 1, NULL),

-- Orphaned OneDrive (departed employee)
('site-guid-0040', 'https://contoso-my.sharepoint.com/personal/departed1_contoso_com',
 'Former Employee 1', 'SPSPERS#10', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-365,@Now),
 15032385536, 1099511627776, 0,
 NULL, NULL, 0,
 NULL, NULL, NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-370,@Now), 0, 1, NULL),

('site-guid-0041', 'https://contoso-my.sharepoint.com/personal/eve_contoso_com',
 'Eve Davis', 'SPSPERS#10', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-5,@Now),
 8589934592, 1099511627776, 0,
 'label-gen-001', 'General', 0,
 'eve@contoso.com', 'Eve Davis', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-7,@Now), 0, 1, NULL),

('site-guid-0042', 'https://contoso-my.sharepoint.com/personal/frank_contoso_com',
 'Frank Wilson', 'SPSPERS#10', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-10,@Now),
 3221225472, 1099511627776, 0,
 NULL, NULL, 1,
 'frank@contoso.com', 'Frank Wilson', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-12,@Now), 0, 1, NULL),

('site-guid-0043', 'https://contoso-my.sharepoint.com/personal/grace_contoso_com',
 'Grace Lee', 'SPSPERS#10', DATEADD(MONTH,-8,@Now), DATEADD(DAY,-15,@Now),
 4294967296, 1099511627776, 0,
 'label-conf-001', 'Confidential', 0,
 'grace@contoso.com', 'Grace Lee', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-18,@Now), 0, 1, NULL),

-- Read-locked OneDrive
('site-guid-0044', 'https://contoso-my.sharepoint.com/personal/departed2_contoso_com',
 'Former Employee 2', 'SPSPERS#10', DATEADD(YEAR,-3,@Now), DATEADD(DAY,-500,@Now),
 21474836480, 1099511627776, 0,
 NULL, NULL, 0,
 NULL, NULL, NULL, 0, 1, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-510,@Now), 0, 1, NULL),

('site-guid-0045', 'https://contoso-my.sharepoint.com/personal/henry_contoso_com',
 'Henry Taylor', 'SPSPERS#10', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-1,@Now),
 16106127360, 1099511627776, 0,
 'label-gen-001', 'General', 0,
 'henry@contoso.com', 'Henry Taylor', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-3,@Now), 0, 1, NULL),

('site-guid-0046', 'https://contoso-my.sharepoint.com/personal/irene_contoso_com',
 'Irene Martin', 'SPSPERS#10', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-7,@Now),
 6442450944, 1099511627776, 0,
 NULL, NULL, 0,
 'irene@contoso.com', 'Irene Martin', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 0, 1, NULL),

('site-guid-0047', 'https://contoso-my.sharepoint.com/personal/jack_contoso_com',
 'Jack Anderson', 'SPSPERS#10', DATEADD(MONTH,-6,@Now), DATEADD(DAY,-20,@Now),
 2147483648, 1099511627776, 0,
 'label-gen-001', 'General', 0,
 'jack@contoso.com', 'Jack Anderson', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-22,@Now), 0, 1, NULL),

('site-guid-0048', 'https://contoso-my.sharepoint.com/personal/karen_contoso_com',
 'Karen Thomas', 'SPSPERS#10', DATEADD(YEAR,-2,@Now), DATEADD(DAY,-4,@Now),
 12884901888, 1099511627776, 0,
 'label-conf-001', 'Confidential', 0,
 'karen@contoso.com', 'Karen Thomas', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-6,@Now), 0, 1, NULL),

-- External sharing OneDrive
('site-guid-0049', 'https://contoso-my.sharepoint.com/personal/larry_contoso_com',
 'Larry Jackson', 'SPSPERS#10', DATEADD(YEAR,-4,@Now), DATEADD(DAY,-2,@Now),
 7516192768, 1099511627776, 0,
 NULL, NULL, 1,
 'larry@contoso.com', 'Larry Jackson', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-4,@Now), 0, 1, NULL),

('site-guid-0050', 'https://contoso-my.sharepoint.com/personal/mary_contoso_com',
 'Mary Harris', 'SPSPERS#10', DATEADD(YEAR,-1,@Now), DATEADD(DAY,-8,@Now),
 4831838208, 1099511627776, 0,
 'label-gen-001', 'General', 0,
 'mary@contoso.com', 'Mary Harris', NULL, 0, 0, NULL,
 0, 'NAM', @Snap, DATEADD(DAY,-10,@Now), 0, 1, NULL);

PRINT 'Inserted 50 SPOSites rows.';
GO

-- ============================================================
-- 2. SPOFiles — 500 files
-- Mix of extensions, sizes, labels, versions, stale/fresh
-- Uses a numbers CTE to generate rows efficiently
-- ============================================================

DECLARE @Snap DATETIME2 = CAST(GETDATE() AS DATE);
DECLARE @Now  DATETIME2 = GETDATE();

-- Generate 500 files across the 50 sites (10 per site)
;WITH Nums AS (
    SELECT TOP 500 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS N
    FROM sys.objects a CROSS JOIN sys.objects b
),
SiteNums AS (
    SELECT N,
        -- Map file to site: file 1-10 -> site 1, file 11-20 -> site 2, etc.
        'site-guid-' + RIGHT('0000' + CAST(((N-1)/10)+1 AS VARCHAR), 4) AS SiteId,
        'item-guid-' + RIGHT('0000' + CAST(N AS VARCHAR), 4) AS ItemId,
        ((N-1) % 10) + 1 AS FileIdx,
        ((N-1)/10)+1 AS SiteNum
    FROM Nums
)
INSERT INTO dbo.SPOFiles (
    SiteId, ItemId, FileName, Extension, SizeInBytes, SizeInBytesWithVersions,
    TimeCreated, TimeLastModified, [Author.Email], [Author.Name],
    [ModifiedBy.Email], [ModifiedBy.Name],
    [SensitivityLabelInfo.Id], [SensitivityLabelInfo.DisplayName],
    IsLabelEncrypted, MajorVersion, MinorVersion, DirName, SiteUrl, WebId, ListId, SnapshotDate
)
SELECT
    SiteId,
    ItemId,
    -- File names vary by index
    CASE FileIdx
        WHEN 1 THEN 'Budget_2026.xlsx'
        WHEN 2 THEN 'Project_Plan.docx'
        WHEN 3 THEN 'Presentation.pptx'
        WHEN 4 THEN 'Report.pdf'
        WHEN 5 THEN 'Photo_001.jpg'
        WHEN 6 THEN 'Data_Export.csv'
        WHEN 7 THEN 'Meeting_Notes.docx'
        WHEN 8 THEN 'Architecture_Diagram.png'
        WHEN 9 THEN 'Policy_Document.pdf'
        WHEN 10 THEN 'Training_Video.mp4'
    END,
    -- Extensions
    CASE FileIdx
        WHEN 1 THEN '.xlsx' WHEN 2 THEN '.docx' WHEN 3 THEN '.pptx'
        WHEN 4 THEN '.pdf' WHEN 5 THEN '.jpg' WHEN 6 THEN '.csv'
        WHEN 7 THEN '.docx' WHEN 8 THEN '.png' WHEN 9 THEN '.pdf'
        WHEN 10 THEN '.mp4'
    END,
    -- SizeInBytes: vary significantly
    CASE FileIdx
        WHEN 1 THEN 2097152      -- 2 MB
        WHEN 2 THEN 524288       -- 512 KB
        WHEN 3 THEN 15728640     -- 15 MB
        WHEN 4 THEN 1048576      -- 1 MB
        WHEN 5 THEN 3145728      -- 3 MB
        WHEN 6 THEN 10485760     -- 10 MB
        WHEN 7 THEN 262144       -- 256 KB
        WHEN 8 THEN 5242880      -- 5 MB
        WHEN 9 THEN 838860       -- ~800 KB
        -- Large file for risk scoring: 200 MB
        WHEN 10 THEN CASE WHEN SiteNum % 3 = 0 THEN 209715200 ELSE 52428800 END
    END,
    -- SizeInBytesWithVersions: some have version bloat (>10x)
    CASE FileIdx
        WHEN 1 THEN CASE WHEN SiteNum % 5 = 0 THEN 2097152 * 15 ELSE 2097152 * 3 END
        WHEN 2 THEN 524288 * 4
        WHEN 3 THEN 15728640 * 2
        WHEN 4 THEN 1048576 * 2
        WHEN 5 THEN 3145728
        WHEN 6 THEN CASE WHEN SiteNum % 4 = 0 THEN 10485760 * 12 ELSE 10485760 * 2 END
        WHEN 7 THEN 262144 * 5
        WHEN 8 THEN 5242880 * 2
        WHEN 9 THEN 838860 * 3
        WHEN 10 THEN CASE WHEN SiteNum % 3 = 0 THEN 209715200 * 2 ELSE 52428800 * 2 END
    END,
    -- TimeCreated: spread across various ages
    DATEADD(DAY, -(N % 800), @Now),
    -- TimeLastModified: some stale (>180 days), some fresh
    CASE
        WHEN FileIdx IN (4,9) AND SiteNum % 3 = 0 THEN DATEADD(DAY, -250, @Now)  -- stale
        WHEN FileIdx = 5 AND SiteNum % 5 = 0 THEN DATEADD(DAY, -400, @Now)       -- ancient
        ELSE DATEADD(DAY, -(N % 120), @Now)                                         -- recent
    END,
    -- Author
    CASE (SiteNum % 10)
        WHEN 1 THEN 'alice@contoso.com' WHEN 2 THEN 'bob@contoso.com'
        WHEN 3 THEN 'carol@contoso.com' WHEN 4 THEN 'dave@contoso.com'
        WHEN 5 THEN 'eve@contoso.com'   WHEN 6 THEN 'frank@contoso.com'
        WHEN 7 THEN 'grace@contoso.com' WHEN 8 THEN 'henry@contoso.com'
        WHEN 9 THEN 'irene@contoso.com' ELSE 'jack@contoso.com'
    END,
    CASE (SiteNum % 10)
        WHEN 1 THEN 'Alice Johnson'   WHEN 2 THEN 'Bob Smith'
        WHEN 3 THEN 'Carol White'     WHEN 4 THEN 'Dave Brown'
        WHEN 5 THEN 'Eve Davis'       WHEN 6 THEN 'Frank Wilson'
        WHEN 7 THEN 'Grace Lee'       WHEN 8 THEN 'Henry Taylor'
        WHEN 9 THEN 'Irene Martin'    ELSE 'Jack Anderson'
    END,
    -- ModifiedBy (sometimes different from author)
    CASE ((SiteNum + FileIdx) % 10)
        WHEN 1 THEN 'alice@contoso.com' WHEN 2 THEN 'bob@contoso.com'
        WHEN 3 THEN 'carol@contoso.com' WHEN 4 THEN 'dave@contoso.com'
        WHEN 5 THEN 'eve@contoso.com'   WHEN 6 THEN 'frank@contoso.com'
        WHEN 7 THEN 'grace@contoso.com' WHEN 8 THEN 'henry@contoso.com'
        WHEN 9 THEN 'irene@contoso.com' ELSE 'jack@contoso.com'
    END,
    CASE ((SiteNum + FileIdx) % 10)
        WHEN 1 THEN 'Alice Johnson'   WHEN 2 THEN 'Bob Smith'
        WHEN 3 THEN 'Carol White'     WHEN 4 THEN 'Dave Brown'
        WHEN 5 THEN 'Eve Davis'       WHEN 6 THEN 'Frank Wilson'
        WHEN 7 THEN 'Grace Lee'       WHEN 8 THEN 'Henry Taylor'
        WHEN 9 THEN 'Irene Martin'    ELSE 'Jack Anderson'
    END,
    -- SensitivityLabelInfo: ~60% labeled
    CASE
        WHEN FileIdx IN (1,2,7,9) AND SiteNum % 3 <> 0 THEN 'label-conf-001'
        WHEN FileIdx IN (3,6) AND SiteNum % 2 = 0 THEN 'label-gen-001'
        WHEN FileIdx = 4 AND SiteNum <= 15 THEN 'label-hbi-001'
        ELSE NULL
    END,
    CASE
        WHEN FileIdx IN (1,2,7,9) AND SiteNum % 3 <> 0 THEN 'Confidential'
        WHEN FileIdx IN (3,6) AND SiteNum % 2 = 0 THEN 'General'
        WHEN FileIdx = 4 AND SiteNum <= 15 THEN 'Highly Confidential'
        ELSE NULL
    END,
    -- IsLabelEncrypted: only some labeled files are encrypted
    CASE
        WHEN FileIdx IN (1,2,7,9) AND SiteNum % 3 <> 0 AND SiteNum % 2 = 0 THEN 1
        WHEN FileIdx = 4 AND SiteNum <= 15 THEN 1
        ELSE 0
    END,
    -- MajorVersion
    CASE WHEN SiteNum % 5 = 0 THEN 25 ELSE (FileIdx * 2) + (SiteNum % 5) END,
    -- MinorVersion
    CASE WHEN FileIdx % 3 = 0 THEN 0 ELSE FileIdx % 3 END,
    -- DirName: some in External/Shared paths for risk scoring
    CASE
        WHEN FileIdx = 6 AND SiteNum % 4 = 0 THEN 'sites/' + CAST(SiteNum AS VARCHAR) + '/Shared Documents/External/'
        WHEN FileIdx = 10 AND SiteNum % 5 = 0 THEN 'sites/' + CAST(SiteNum AS VARCHAR) + '/Shared Documents/Shared with Everyone/'
        ELSE 'sites/' + CAST(SiteNum AS VARCHAR) + '/Shared Documents/General/'
    END,
    -- SiteUrl
    'https://contoso.sharepoint.com/sites/Site' + CAST(SiteNum AS VARCHAR),
    -- WebId
    'web-guid-' + RIGHT('0000' + CAST(SiteNum AS VARCHAR), 4),
    -- ListId
    'list-guid-' + RIGHT('0000' + CAST(SiteNum AS VARCHAR), 4),
    @Snap
FROM SiteNums;

PRINT 'Inserted 500 SPOFiles rows.';
GO

-- ============================================================
-- 3. SPOFileActions — 2000 actions
-- Mix: FileAccessed/FileModified/FileDeleted/SharingSet etc.
-- Internal + external actors, after-hours, weekends
-- ============================================================

DECLARE @Snap DATETIME2 = CAST(GETDATE() AS DATE);
DECLARE @Now  DATETIME2 = GETDATE();

;WITH Nums AS (
    SELECT TOP 2000 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS N
    FROM sys.objects a CROSS JOIN sys.objects b CROSS JOIN sys.objects c
)
INSERT INTO dbo.SPOFileActions (
    SiteId, SiteUrl, WebId, ListId, ListItemId,
    ItemURL, ItemName, ItemExtension,
    ActionDate, ActorType, ActorIdType, ActorDisplayName, ActorEmail,
    ActionName, UserAgent, ClientIP, SnapshotDate
)
SELECT
    -- Distribute across first 30 sites
    'site-guid-' + RIGHT('0000' + CAST(((N-1) % 30)+1 AS VARCHAR), 4),
    'https://contoso.sharepoint.com/sites/Site' + CAST(((N-1) % 30)+1 AS VARCHAR),
    'web-guid-' + RIGHT('0000' + CAST(((N-1) % 30)+1 AS VARCHAR), 4),
    'list-guid-' + RIGHT('0000' + CAST(((N-1) % 30)+1 AS VARCHAR), 4),
    'item-guid-' + RIGHT('0000' + CAST(((N-1) % 500)+1 AS VARCHAR), 4),
    'https://contoso.sharepoint.com/sites/Site' + CAST(((N-1) % 30)+1 AS VARCHAR) + '/doc' + CAST(N AS VARCHAR),
    CASE (N % 8)
        WHEN 0 THEN 'Budget_2026.xlsx'     WHEN 1 THEN 'Project_Plan.docx'
        WHEN 2 THEN 'Presentation.pptx'    WHEN 3 THEN 'Report.pdf'
        WHEN 4 THEN 'Data_Export.csv'       WHEN 5 THEN 'Meeting_Notes.docx'
        WHEN 6 THEN 'Policy_Document.pdf'   WHEN 7 THEN 'Architecture_Diagram.png'
    END,
    CASE (N % 8)
        WHEN 0 THEN '.xlsx' WHEN 1 THEN '.docx' WHEN 2 THEN '.pptx'
        WHEN 3 THEN '.pdf'  WHEN 4 THEN '.csv'  WHEN 5 THEN '.docx'
        WHEN 6 THEN '.pdf'  WHEN 7 THEN '.png'
    END,
    -- ActionDate: spread across last 90 days with time variation
    -- Some after-hours (before 7 AM or after 7 PM), some weekends
    DATEADD(MINUTE,
        CASE
            WHEN N % 20 = 0 THEN (3 * 60)     -- 3 AM (after hours)
            WHEN N % 15 = 0 THEN (22 * 60)    -- 10 PM (after hours)
            WHEN N % 10 = 0 THEN (5 * 60)     -- 5 AM (after hours)
            ELSE (9 * 60) + (N % 480)          -- 9 AM to 5 PM spread
        END,
        CAST(DATEADD(DAY, -(N % 90), CAST(@Now AS DATE)) AS DATETIME2)
    ),
    -- ActorType: ~10% external
    CASE WHEN N % 10 = 0 THEN 'External' ELSE 'Internal' END,
    -- ActorIdType
    CASE WHEN N % 10 = 0 THEN 'ExternalUser' ELSE 'AzureAD' END,
    -- ActorDisplayName
    CASE
        WHEN N % 10 = 0 THEN CASE (N % 5)
            WHEN 0 THEN 'External Partner A'  WHEN 1 THEN 'Vendor Contact B'
            WHEN 2 THEN 'Client User C'       WHEN 3 THEN 'Contractor D'
            ELSE 'Guest User E'
        END
        ELSE CASE (N % 10)
            WHEN 1 THEN 'Alice Johnson'   WHEN 2 THEN 'Bob Smith'
            WHEN 3 THEN 'Carol White'     WHEN 4 THEN 'Dave Brown'
            WHEN 5 THEN 'Eve Davis'       WHEN 6 THEN 'Frank Wilson'
            WHEN 7 THEN 'Grace Lee'       WHEN 8 THEN 'Henry Taylor'
            WHEN 9 THEN 'Irene Martin'    ELSE 'Jack Anderson'
        END
    END,
    -- ActorEmail
    CASE
        WHEN N % 10 = 0 THEN CASE (N % 5)
            WHEN 0 THEN 'partner.a@external.com'  WHEN 1 THEN 'vendor.b@partner.com'
            WHEN 2 THEN 'client.c@customer.com'   WHEN 3 THEN 'contractor.d@agency.com'
            ELSE 'guest.e@personal.com'
        END
        ELSE CASE (N % 10)
            WHEN 1 THEN 'alice@contoso.com'   WHEN 2 THEN 'bob@contoso.com'
            WHEN 3 THEN 'carol@contoso.com'   WHEN 4 THEN 'dave@contoso.com'
            WHEN 5 THEN 'eve@contoso.com'     WHEN 6 THEN 'frank@contoso.com'
            WHEN 7 THEN 'grace@contoso.com'   WHEN 8 THEN 'henry@contoso.com'
            WHEN 9 THEN 'irene@contoso.com'   ELSE 'jack@contoso.com'
        END
    END,
    -- ActionName: weighted distribution
    CASE
        WHEN N % 100 < 40 THEN 'FileAccessed'           -- 40%
        WHEN N % 100 < 65 THEN 'FileModified'           -- 25%
        WHEN N % 100 < 75 THEN 'FileUploaded'           -- 10%
        WHEN N % 100 < 82 THEN 'FileDeleted'            -- 7%
        WHEN N % 100 < 88 THEN 'SharingSet'             -- 6%
        WHEN N % 100 < 92 THEN 'PermissionChanged'      -- 4%
        WHEN N % 100 < 95 THEN 'FileCheckedOut'         -- 3%
        WHEN N % 100 < 97 THEN 'FileCheckedIn'          -- 2%
        WHEN N % 100 < 99 THEN 'FileVersionsAllDeleted' -- 2%
        ELSE 'FileMalwareDetected'                       -- 1%
    END,
    -- UserAgent: mix of clients
    CASE (N % 6)
        WHEN 0 THEN 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0'
        WHEN 1 THEN 'Microsoft Teams/1.6.00.33'
        WHEN 2 THEN 'OneDrive/24.001.0'
        WHEN 3 THEN 'Mozilla/5.0 Chrome/120.0.0.0'
        WHEN 4 THEN 'CSOM/16.0.0.0'
        WHEN 5 THEN 'Microsoft Office Mobile/16.0'
    END,
    -- ClientIP
    CASE
        WHEN N % 10 = 0 THEN '203.0.113.' + CAST((N % 254)+1 AS VARCHAR)  -- external IPs
        ELSE '10.0.' + CAST(N % 255 AS VARCHAR) + '.' + CAST((N % 254)+1 AS VARCHAR)
    END,
    @Snap
FROM Nums;

PRINT 'Inserted 2000 SPOFileActions rows.';
GO

-- ============================================================
-- 4. SPOPermissions — 1000 permissions
-- Mix: Anyone/Organization/SpecificPeople/Direct link scopes
-- Various roles, expired and never-expiring links
-- ============================================================

DECLARE @Snap DATETIME2 = CAST(GETDATE() AS DATE);
DECLARE @Now  DATETIME2 = GETDATE();

;WITH Nums AS (
    SELECT TOP 1000 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS N
    FROM sys.objects a CROSS JOIN sys.objects b
)
INSERT INTO dbo.SPOPermissions (
    SiteId, WebId, ListId, ListItemId, UniqueId,
    ItemType, ItemURL, FileExtension,
    RoleDefinition, LinkId, ScopeId, LinkScope, TotalUserCount,
    [ShareCreatedBy.Email], [ShareCreatedBy.Name],
    ShareCreatedTime,
    [ShareLastModifiedBy.Email], [ShareLastModifiedBy.Name],
    ShareLastModifiedTime, ShareExpirationTime, SnapshotDate
)
SELECT
    'site-guid-' + RIGHT('0000' + CAST(((N-1) % 50)+1 AS VARCHAR), 4),
    'web-guid-' + RIGHT('0000' + CAST(((N-1) % 50)+1 AS VARCHAR), 4),
    'list-guid-' + RIGHT('0000' + CAST(((N-1) % 50)+1 AS VARCHAR), 4),
    'item-guid-' + RIGHT('0000' + CAST(((N-1) % 500)+1 AS VARCHAR), 4),
    'perm-guid-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    -- ItemType
    CASE WHEN N % 5 = 0 THEN 'Folder' ELSE 'File' END,
    -- ItemURL
    'https://contoso.sharepoint.com/sites/Site' + CAST(((N-1) % 50)+1 AS VARCHAR) + '/doc' + CAST(N AS VARCHAR),
    -- FileExtension
    CASE (N % 5)
        WHEN 0 THEN NULL        -- folders
        WHEN 1 THEN '.docx'
        WHEN 2 THEN '.xlsx'
        WHEN 3 THEN '.pdf'
        WHEN 4 THEN '.pptx'
    END,
    -- RoleDefinition
    CASE (N % 10)
        WHEN 0 THEN 'Full Control'
        WHEN 1 THEN 'Write'     WHEN 2 THEN 'Write'
        WHEN 3 THEN 'Read'      WHEN 4 THEN 'Read'
        WHEN 5 THEN 'Read'      WHEN 6 THEN 'Read'
        WHEN 7 THEN 'Write'     WHEN 8 THEN 'Read'
        WHEN 9 THEN 'Read'
    END,
    -- LinkId
    'link-guid-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    -- ScopeId
    'scope-guid-' + RIGHT('0000' + CAST(((N-1) % 200)+1 AS VARCHAR), 4),
    -- LinkScope: critical distribution for risk scoring
    CASE
        WHEN N % 20 = 0 THEN 'Anyone'             -- 5% anonymous
        WHEN N % 10 < 3 THEN 'Organization'        -- 25% org-wide
        WHEN N % 10 < 6 THEN 'SpecificPeople'      -- 30% specific
        WHEN N % 10 < 8 THEN NULL                   -- 20% direct (no link)
        ELSE 'SpecificPeople'                        -- 20% specific
    END,
    -- TotalUserCount
    CASE
        WHEN N % 20 = 0 THEN 0                     -- anyone links: 0 explicit users
        WHEN N % 10 < 3 THEN 0                     -- org-wide
        ELSE (N % 15) + 1                           -- 1-15 users
    END,
    -- ShareCreatedBy
    CASE (N % 10)
        WHEN 0 THEN 'alice@contoso.com'   WHEN 1 THEN 'bob@contoso.com'
        WHEN 2 THEN 'carol@contoso.com'   WHEN 3 THEN 'dave@contoso.com'
        WHEN 4 THEN 'eve@contoso.com'     WHEN 5 THEN 'frank@contoso.com'
        WHEN 6 THEN 'grace@contoso.com'   WHEN 7 THEN 'henry@contoso.com'
        WHEN 8 THEN 'irene@contoso.com'   WHEN 9 THEN 'jack@contoso.com'
    END,
    CASE (N % 10)
        WHEN 0 THEN 'Alice Johnson'   WHEN 1 THEN 'Bob Smith'
        WHEN 2 THEN 'Carol White'     WHEN 3 THEN 'Dave Brown'
        WHEN 4 THEN 'Eve Davis'       WHEN 5 THEN 'Frank Wilson'
        WHEN 6 THEN 'Grace Lee'       WHEN 7 THEN 'Henry Taylor'
        WHEN 8 THEN 'Irene Martin'    WHEN 9 THEN 'Jack Anderson'
    END,
    -- ShareCreatedTime: spread across last 2 years
    DATEADD(DAY, -(N % 730), @Now),
    -- ShareLastModifiedBy (same as creator for simplicity)
    CASE (N % 10)
        WHEN 0 THEN 'alice@contoso.com'   WHEN 1 THEN 'bob@contoso.com'
        WHEN 2 THEN 'carol@contoso.com'   WHEN 3 THEN 'dave@contoso.com'
        WHEN 4 THEN 'eve@contoso.com'     WHEN 5 THEN 'frank@contoso.com'
        WHEN 6 THEN 'grace@contoso.com'   WHEN 7 THEN 'henry@contoso.com'
        WHEN 8 THEN 'irene@contoso.com'   WHEN 9 THEN 'jack@contoso.com'
    END,
    CASE (N % 10)
        WHEN 0 THEN 'Alice Johnson'   WHEN 1 THEN 'Bob Smith'
        WHEN 2 THEN 'Carol White'     WHEN 3 THEN 'Dave Brown'
        WHEN 4 THEN 'Eve Davis'       WHEN 5 THEN 'Frank Wilson'
        WHEN 6 THEN 'Grace Lee'       WHEN 7 THEN 'Henry Taylor'
        WHEN 8 THEN 'Irene Martin'    WHEN 9 THEN 'Jack Anderson'
    END,
    DATEADD(DAY, -(N % 365), @Now),
    -- ShareExpirationTime: mix of NULL (never expires), past, near-future, far-future
    CASE
        WHEN N % 5 = 0 THEN NULL                            -- 20% never expires
        WHEN N % 20 = 1 THEN DATEADD(DAY, -30, @Now)        -- expired 30 days ago
        WHEN N % 20 = 3 THEN DATEADD(DAY, 15, @Now)         -- expiring soon (15 days)
        WHEN N % 20 = 7 THEN DATEADD(DAY, 7, @Now)          -- expiring very soon (7 days)
        ELSE DATEADD(DAY, 90 + (N % 365), @Now)              -- future expiration
    END,
    @Snap
FROM Nums;

PRINT 'Inserted 1000 SPOPermissions rows.';
GO

-- ============================================================
-- 5. SPOGroups — 100 groups
-- Mix: SecurityGroup/M365Group/SharePointGroup
-- Some ownerless for risk scoring
-- ============================================================

DECLARE @Snap DATETIME2 = CAST(GETDATE() AS DATE);

;WITH Nums AS (
    SELECT TOP 100 ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS N
    FROM sys.objects a
)
INSERT INTO dbo.SPOGroups (
    SiteId, GroupId, GroupLinkId, GroupType, DisplayName,
    [Owner.Email], [Owner.Name], [Owner.Type], SnapshotDate
)
SELECT
    'site-guid-' + RIGHT('0000' + CAST(((N-1) % 50)+1 AS VARCHAR), 4),
    N,  -- GroupId (BIGINT)
    'grplink-guid-' + RIGHT('0000' + CAST(N AS VARCHAR), 4),
    -- GroupType distribution
    CASE
        WHEN N % 5 = 0 THEN 'SecurityGroup'        -- 20%
        WHEN N % 5 < 3 THEN 'M365Group'            -- 40%
        ELSE 'SharePointGroup'                       -- 40%
    END,
    -- DisplayName
    CASE (N % 10)
        WHEN 0 THEN 'Site Owners'
        WHEN 1 THEN 'Site Members'
        WHEN 2 THEN 'Site Visitors'
        WHEN 3 THEN 'External Sharing Group'
        WHEN 4 THEN 'Project Team A'
        WHEN 5 THEN 'Security Admins'
        WHEN 6 THEN 'Department Leads'
        WHEN 7 THEN 'All Company'
        WHEN 8 THEN 'Contractor Access'
        WHEN 9 THEN 'Read Only Users'
    END + ' - Site ' + CAST(((N-1) % 50)+1 AS VARCHAR),
    -- Owner.Email: ~20% ownerless
    CASE
        WHEN N % 5 = 0 AND N % 10 <> 5 THEN NULL  -- ownerless security groups (Critical risk)
        WHEN N % 7 = 0 THEN NULL                    -- other ownerless groups (High risk)
        ELSE CASE (N % 10)
            WHEN 0 THEN 'alice@contoso.com'   WHEN 1 THEN 'bob@contoso.com'
            WHEN 2 THEN 'carol@contoso.com'   WHEN 3 THEN 'dave@contoso.com'
            WHEN 4 THEN 'eve@contoso.com'     WHEN 5 THEN 'frank@contoso.com'
            WHEN 6 THEN 'grace@contoso.com'   WHEN 7 THEN 'henry@contoso.com'
            WHEN 8 THEN 'irene@contoso.com'   WHEN 9 THEN 'jack@contoso.com'
        END
    END,
    CASE
        WHEN N % 5 = 0 AND N % 10 <> 5 THEN NULL
        WHEN N % 7 = 0 THEN NULL
        ELSE CASE (N % 10)
            WHEN 0 THEN 'Alice Johnson'   WHEN 1 THEN 'Bob Smith'
            WHEN 2 THEN 'Carol White'     WHEN 3 THEN 'Dave Brown'
            WHEN 4 THEN 'Eve Davis'       WHEN 5 THEN 'Frank Wilson'
            WHEN 6 THEN 'Grace Lee'       WHEN 7 THEN 'Henry Taylor'
            WHEN 8 THEN 'Irene Martin'    WHEN 9 THEN 'Jack Anderson'
        END
    END,
    -- Owner.Type
    CASE
        WHEN N % 5 = 0 AND N % 10 <> 5 THEN NULL
        WHEN N % 7 = 0 THEN NULL
        WHEN N % 3 = 0 THEN 'SecurityGroup'
        ELSE 'User'
    END,
    @Snap
FROM Nums;

PRINT 'Inserted 100 SPOGroups rows.';
GO

-- ============================================================
-- Verification queries
-- ============================================================
SELECT 'SPOSites' AS TableName, COUNT(*) AS RowCount FROM dbo.SPOSites
UNION ALL SELECT 'SPOFiles', COUNT(*) FROM dbo.SPOFiles
UNION ALL SELECT 'SPOFileActions', COUNT(*) FROM dbo.SPOFileActions
UNION ALL SELECT 'SPOPermissions', COUNT(*) FROM dbo.SPOPermissions
UNION ALL SELECT 'SPOGroups', COUNT(*) FROM dbo.SPOGroups;
GO

PRINT 'Seed data insertion complete.';
GO
