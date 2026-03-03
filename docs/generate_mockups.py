#!/usr/bin/env python3
"""Generate Power BI dashboard mockup images for all 10 report pages."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'mockups')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color scheme (Power BI dark theme inspired)
BG_COLOR = '#1B1B2F'
CARD_BG = '#162447'
CARD_BORDER = '#1F4068'
ACCENT_BLUE = '#1B98E0'
ACCENT_RED = '#E94560'
ACCENT_GREEN = '#0CCE6B'
ACCENT_YELLOW = '#FFC857'
ACCENT_ORANGE = '#FF6B35'
ACCENT_PURPLE = '#9B5DE5'
TEXT_WHITE = '#FFFFFF'
TEXT_GRAY = '#A0A0B0'
TEXT_DIM = '#6B6B80'
CHART_BG = '#162447'
TABLE_HEADER = '#1F4068'
TABLE_ROW1 = '#1A2744'
TABLE_ROW2 = '#162040'

RISK_COLORS = {
    'Critical': ACCENT_RED,
    'High': ACCENT_ORANGE,
    'Medium': ACCENT_YELLOW,
    'Low': ACCENT_GREEN,
}

def create_figure():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(BG_COLOR)
    return fig

def add_page_title(fig, title, subtitle=""):
    fig.text(0.02, 0.96, title, fontsize=22, fontweight='bold',
             color=TEXT_WHITE, fontfamily='sans-serif', va='top')
    if subtitle:
        fig.text(0.02, 0.925, subtitle, fontsize=11, color=TEXT_GRAY, va='top')

def draw_card(fig, x, y, w, h, label, value, color=ACCENT_BLUE, value_size=28):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
        spine.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    # Color accent bar at top
    ax.axhline(y=1, color=color, linewidth=4, xmin=0.05, xmax=0.95)
    ax.text(0.5, 0.55, str(value), fontsize=value_size, fontweight='bold',
            color=color, ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.15, label, fontsize=9, color=TEXT_GRAY,
            ha='center', va='center', transform=ax.transAxes, wrap=True)

def draw_bar_chart(fig, x, y, w, h, title, categories, values, colors=None, horizontal=False):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CHART_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
    ax.tick_params(colors=TEXT_GRAY, labelsize=8)
    ax.set_title(title, fontsize=11, color=TEXT_WHITE, pad=10, loc='left', fontweight='bold')
    if colors is None:
        colors = [ACCENT_BLUE] * len(categories)
    if horizontal:
        bars = ax.barh(range(len(categories)), values, color=colors, edgecolor='none', height=0.6)
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories, fontsize=8, color=TEXT_GRAY)
        ax.invert_yaxis()
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(axis='y', length=0)
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + max(values)*0.02, bar.get_y() + bar.get_height()/2,
                    str(val), va='center', fontsize=8, color=TEXT_GRAY)
    else:
        bars = ax.bar(range(len(categories)), values, color=colors, edgecolor='none', width=0.6)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, fontsize=8, color=TEXT_GRAY, rotation=30, ha='right')
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    ax.grid(axis='x' if horizontal else 'y', color=TEXT_DIM, alpha=0.2, linewidth=0.5)

def draw_donut_chart(fig, x, y, w, h, title, labels, values, colors=None):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CHART_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
    if colors is None:
        colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_YELLOW, ACCENT_ORANGE, ACCENT_RED, ACCENT_PURPLE]
    colors = colors[:len(labels)]
    wedges, _ = ax.pie(values, colors=colors, startangle=90,
                       wedgeprops=dict(width=0.35, edgecolor=CHART_BG, linewidth=2))
    centre_circle = plt.Circle((0,0), 0.45, fc=CHART_BG)
    ax.add_artist(centre_circle)
    ax.set_title(title, fontsize=11, color=TEXT_WHITE, pad=8, loc='left', fontweight='bold')
    # Legend
    total = sum(values)
    legend_labels = [f'{l} ({v/total*100:.0f}%)' for l, v in zip(labels, values)]
    leg = ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.85, 0.5),
                    fontsize=7, frameon=False, labelcolor=TEXT_GRAY)

def draw_line_chart(fig, x, y, w, h, title, x_labels, values, color=ACCENT_BLUE):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CHART_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
    ax.tick_params(colors=TEXT_GRAY, labelsize=8)
    ax.set_title(title, fontsize=11, color=TEXT_WHITE, pad=10, loc='left', fontweight='bold')
    ax.plot(range(len(values)), values, color=color, linewidth=2)
    ax.fill_between(range(len(values)), values, alpha=0.15, color=color)
    ax.set_xticks(range(0, len(x_labels), max(1, len(x_labels)//6)))
    ax.set_xticklabels([x_labels[i] for i in range(0, len(x_labels), max(1, len(x_labels)//6))],
                       fontsize=7, color=TEXT_GRAY, rotation=30, ha='right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color=TEXT_DIM, alpha=0.2, linewidth=0.5)

def draw_gauge(fig, x, y, w, h, title, value, max_val=100):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CHART_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.3, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11, color=TEXT_WHITE, pad=8, loc='left', fontweight='bold')
    # Draw gauge arc segments
    theta_ranges = [(180, 144, ACCENT_RED), (144, 108, ACCENT_ORANGE),
                    (108, 72, ACCENT_YELLOW), (72, 36, ACCENT_GREEN), (36, 0, '#00E676')]
    for start, end, color in theta_ranges:
        angles = np.linspace(np.radians(start), np.radians(end), 30)
        for i in range(len(angles)-1):
            ax.plot([1.1*np.cos(angles[i]), 1.1*np.cos(angles[i+1])],
                    [1.1*np.sin(angles[i]), 1.1*np.sin(angles[i+1])],
                    color=color, linewidth=12, solid_capstyle='butt')
    # Needle
    pct = value / max_val
    angle = np.radians(180 - pct * 180)
    ax.annotate('', xy=(0.9*np.cos(angle), 0.9*np.sin(angle)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=TEXT_WHITE, lw=2))
    ax.text(0, -0.15, f'{value}', fontsize=24, fontweight='bold',
            color=TEXT_WHITE, ha='center', va='center')

def draw_table(fig, x, y, w, h, title, headers, rows):
    ax = fig.add_axes([x, y, w, h])
    ax.set_facecolor(CHART_BG)
    for spine in ax.spines.values():
        spine.set_color(CARD_BORDER)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11, color=TEXT_WHITE, pad=8, loc='left', fontweight='bold')
    n_cols = len(headers)
    n_rows = min(len(rows), 6)
    row_h = 0.85 / (n_rows + 1)
    col_w = 1.0 / n_cols
    # Header
    for j, hdr in enumerate(headers):
        rect = FancyBboxPatch((j*col_w, 1 - row_h - 0.05), col_w, row_h,
                              boxstyle="square,pad=0", facecolor=TABLE_HEADER, edgecolor=CARD_BORDER, linewidth=0.5)
        ax.add_patch(rect)
        ax.text(j*col_w + col_w/2, 1 - row_h/2 - 0.05, hdr, fontsize=7.5,
                color=TEXT_WHITE, ha='center', va='center', fontweight='bold')
    # Data rows
    for i in range(n_rows):
        bg = TABLE_ROW1 if i % 2 == 0 else TABLE_ROW2
        for j, val in enumerate(rows[i]):
            rect = FancyBboxPatch((j*col_w, 1 - (i+2)*row_h - 0.05), col_w, row_h,
                                  boxstyle="square,pad=0", facecolor=bg, edgecolor=CARD_BORDER, linewidth=0.3)
            ax.add_patch(rect)
            color = TEXT_GRAY
            if val in RISK_COLORS:
                color = RISK_COLORS[val]
            ax.text(j*col_w + col_w/2, 1 - (i+1.5)*row_h - 0.05, str(val), fontsize=7,
                    color=color, ha='center', va='center')


# ============================================================
# PAGE 1: Executive Security Overview
# ============================================================
def page_01():
    fig = create_figure()
    add_page_title(fig, "Executive Security Overview",
                   "MGDC SharePoint Security Dashboard - Tenant-wide health at a glance")
    # Cards row 1
    draw_card(fig, 0.02, 0.76, 0.15, 0.13, "Total Sites", "1,247", ACCENT_BLUE)
    draw_card(fig, 0.185, 0.76, 0.15, 0.13, "Total Files", "483K", ACCENT_BLUE)
    draw_card(fig, 0.35, 0.76, 0.15, 0.13, "Total Storage (TB)", "12.4", ACCENT_BLUE)
    draw_card(fig, 0.515, 0.76, 0.15, 0.13, "Total Users", "8,932", ACCENT_BLUE)
    draw_card(fig, 0.68, 0.76, 0.15, 0.13, "Critical Risk Sites", "23", ACCENT_RED)
    draw_card(fig, 0.845, 0.76, 0.14, 0.13, "Total Permissions", "52K", ACCENT_ORANGE)
    # Gauge
    draw_gauge(fig, 0.02, 0.38, 0.23, 0.35, "Security Health Score", 68)
    # Bar chart - risk tiers
    draw_bar_chart(fig, 0.28, 0.38, 0.33, 0.35, "Sites by Risk Tier",
                   ['Critical', 'High', 'Medium', 'Low'],
                   [23, 87, 312, 825],
                   [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN])
    # Line chart - activity trend
    days = [f'Feb {d}' for d in range(1, 29)]
    vals = [120, 145, 132, 89, 34, 28, 156, 178, 165, 143, 98, 45, 31,
            167, 189, 176, 154, 112, 52, 38, 198, 210, 195, 171, 124, 61, 42, 185]
    draw_line_chart(fig, 0.65, 0.38, 0.33, 0.35, "Activity Trend (28 Days)", days, vals)
    # Table
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Critical & High Risk Sites",
               ['Site Name', 'URL', 'Risk Score', 'Risk Tier', 'External Sharing', 'Storage (GB)'],
               [['HR Confidential', 'sites/hr-conf', '92', 'Critical', 'Yes', '45.2'],
                ['Finance Shared', 'sites/finance', '88', 'Critical', 'Yes', '128.7'],
                ['Executive Board', 'sites/exec-board', '85', 'Critical', 'Yes', '23.1'],
                ['Marketing External', 'sites/mktg-ext', '78', 'High', 'Yes', '67.4'],
                ['Legal Documents', 'sites/legal-docs', '75', 'High', 'No', '89.3'],
                ['R&D Projects', 'sites/rd-projects', '72', 'High', 'Yes', '156.8']])
    fig.savefig(os.path.join(OUTPUT_DIR, '01_executive_overview.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 2: External Sharing Exposure
# ============================================================
def page_02():
    fig = create_figure()
    add_page_title(fig, "External Sharing Exposure",
                   "Anonymous links, external shares, and sharing risk analysis")
    # Cards
    draw_card(fig, 0.02, 0.76, 0.15, 0.13, "Anonymous Links", "847", ACCENT_RED)
    draw_card(fig, 0.185, 0.76, 0.15, 0.13, "External Shares", "3,421", ACCENT_ORANGE)
    draw_card(fig, 0.35, 0.76, 0.15, 0.13, "Never Expiring Links", "1,892", ACCENT_RED)
    draw_card(fig, 0.515, 0.76, 0.15, 0.13, "Anon Write Links", "127", ACCENT_RED)
    draw_card(fig, 0.68, 0.76, 0.15, 0.13, "Sites w/ Anyone Links", "34", ACCENT_ORANGE)
    draw_card(fig, 0.845, 0.76, 0.14, 0.13, "External Link Users", "2,156", ACCENT_YELLOW)
    # Donut - link types
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Permission Link Types",
                     ['Direct', 'Organization', 'Specific People', 'Anyone'],
                     [4200, 2800, 1500, 847],
                     [ACCENT_BLUE, ACCENT_GREEN, ACCENT_YELLOW, ACCENT_RED])
    # Bar - top sites
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Top Sites by Anonymous Links",
                   ['Marketing', 'Sales Portal', 'HR Public', 'Support', 'Events'],
                   [234, 178, 145, 112, 89],
                   [ACCENT_RED]*5, horizontal=True)
    # Donut - recipients
    draw_donut_chart(fig, 0.68, 0.38, 0.30, 0.35, "External Shares by Item Type",
                     ['File', 'Folder', 'List', 'Site'],
                     [2100, 780, 340, 201],
                     [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_YELLOW, ACCENT_GREEN])
    # Table
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Sharing Exposure Details",
               ['Site', 'Shared By', 'Link Type', 'Role', 'Risk Level'],
               [['Marketing Hub', 'john@contoso.com', 'Anyone', 'Write', 'Critical'],
                ['Sales Portal', 'sara@contoso.com', 'Anyone', 'Read', 'High'],
                ['HR Public Docs', 'mike@contoso.com', 'Anyone', 'Write', 'Critical'],
                ['Support Files', 'lisa@contoso.com', 'Organization', 'Read', 'Medium'],
                ['Events Portal', 'tom@contoso.com', 'Specific People', 'Write', 'Low'],
                ['Training Docs', 'anna@contoso.com', 'Anyone', 'Read', 'High']])
    fig.savefig(os.path.join(OUTPUT_DIR, '02_external_sharing.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 3: Permission Deep Dive
# ============================================================
def page_03():
    fig = create_figure()
    add_page_title(fig, "Permission Deep Dive",
                   "Role assignments, overprivileged access, and permission sprawl analysis")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "Critical Risk Permissions", "1,247", ACCENT_RED)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "High Risk Permissions", "3,892", ACCENT_ORANGE)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Overprivileged Users", "456", ACCENT_YELLOW)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Permission Sprawl Index", "3.7x", ACCENT_PURPLE)
    # Donut - risk distribution
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Permission Risk Distribution",
                     ['Critical', 'High', 'Medium', 'Low'],
                     [1247, 3892, 8456, 38405],
                     [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN])
    # Bar - by role
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Permissions by Role",
                   ['Read', 'Write', 'Contribute', 'Full Control', 'Edit'],
                   [28400, 12300, 7800, 2100, 1400],
                   [ACCENT_GREEN, ACCENT_YELLOW, ACCENT_BLUE, ACCENT_RED, ACCENT_ORANGE])
    # Donut - link types
    draw_donut_chart(fig, 0.68, 0.38, 0.30, 0.35, "Permission Categories",
                     ['Direct', 'Organization', 'Specific', 'Anyone'],
                     [22000, 15000, 10000, 5000],
                     [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_RED])
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Over-Permissioned Files",
               ['File Name', 'Shared By', 'Role', 'Risk Level', 'Overprivileged'],
               [['Budget_2026.xlsx', 'cfo@contoso.com', 'Full Control', 'Critical', 'Yes'],
                ['Strategy_Draft.docx', 'ceo@contoso.com', 'Write', 'Critical', 'Yes'],
                ['Employee_List.xlsx', 'hr@contoso.com', 'Full Control', 'Critical', 'Yes'],
                ['Vendor_Contracts.pdf', 'legal@contoso.com', 'Write', 'High', 'Yes'],
                ['Sales_Pipeline.xlsx', 'sales@contoso.com', 'Write', 'High', 'No'],
                ['Project_Plan.docx', 'pm@contoso.com', 'Read', 'Low', 'No']])
    fig.savefig(os.path.join(OUTPUT_DIR, '03_permission_deep_dive.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 4: Sensitivity & Encryption
# ============================================================
def page_04():
    fig = create_figure()
    add_page_title(fig, "Sensitivity & Encryption",
                   "Data classification coverage, encryption status, and protection gaps")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "File Label Coverage", "34%", ACCENT_ORANGE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Encrypted Files", "12%", ACCENT_RED)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Unprotected Files", "66%", ACCENT_RED)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Sensitive + External", "892", ACCENT_RED)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Sensitivity Label Distribution",
                     ['Confidential', 'Internal', 'Public', 'None'],
                     [8200, 12500, 3800, 458500],
                     [ACCENT_RED, ACCENT_YELLOW, ACCENT_GREEN, TEXT_DIM])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "File Protection Status",
                   ['Protected', 'Encrypted Only', 'Labeled Only', 'Unprotected'],
                   [5800, 2400, 15200, 459600],
                   [ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_RED])
    draw_bar_chart(fig, 0.68, 0.38, 0.30, 0.35, "Unprotected Files by Site",
                   ['Engineering', 'Marketing', 'Finance', 'HR', 'Sales'],
                   [45200, 38900, 32100, 28700, 25400],
                   [ACCENT_RED]*5, horizontal=True)
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Protection Gap Analysis",
               ['Site', 'Label Coverage %', 'Encrypted %', 'Unprotected Files'],
               [['Engineering Hub', '12%', '5%', '45,200'],
                ['Marketing Assets', '18%', '8%', '38,900'],
                ['Finance Shared', '45%', '32%', '32,100'],
                ['HR Confidential', '67%', '55%', '28,700'],
                ['Sales Collateral', '22%', '10%', '25,400'],
                ['Legal Library', '78%', '65%', '12,300']])
    fig.savefig(os.path.join(OUTPUT_DIR, '04_sensitivity_encryption.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 5: User Activity & Anomalies
# ============================================================
def page_05():
    fig = create_figure()
    add_page_title(fig, "User Activity & Anomalies",
                   "File operations, after-hours access, and suspicious behavior detection")
    draw_card(fig, 0.02, 0.76, 0.127, 0.13, "Downloads", "45.2K", ACCENT_BLUE)
    draw_card(fig, 0.16, 0.76, 0.127, 0.13, "Uploads", "23.1K", ACCENT_GREEN)
    draw_card(fig, 0.30, 0.76, 0.127, 0.13, "Deletes", "8,734", ACCENT_RED)
    draw_card(fig, 0.44, 0.76, 0.127, 0.13, "After Hours %", "18%", ACCENT_ORANGE)
    draw_card(fig, 0.58, 0.76, 0.127, 0.13, "Suspicious", "127", ACCENT_RED)
    draw_card(fig, 0.72, 0.76, 0.127, 0.13, "Ext Downloads", "3,456", ACCENT_ORANGE)
    draw_card(fig, 0.86, 0.76, 0.127, 0.13, "Unique IPs", "12.4K", ACCENT_PURPLE)
    # Line - daily trend
    days = [f'Feb {d}' for d in range(1, 29)]
    vals = [2100, 2450, 2300, 1800, 890, 650, 2600, 2800, 2650, 2400, 1950, 980, 720,
            2750, 3100, 2900, 2550, 2100, 1050, 780, 3200, 3400, 3150, 2700, 2200, 1100, 850, 2900]
    draw_line_chart(fig, 0.02, 0.38, 0.45, 0.35, "Daily Activity Trend", days, vals)
    # Bar - action categories
    draw_bar_chart(fig, 0.50, 0.55, 0.23, 0.18, "Actions by Category",
                   ['Read', 'Write', 'Delete', 'Manage'],
                   [45200, 23100, 8734, 4566],
                   [ACCENT_GREEN, ACCENT_BLUE, ACCENT_RED, ACCENT_PURPLE])
    # Bar - client apps
    draw_bar_chart(fig, 0.76, 0.55, 0.22, 0.18, "Client Applications",
                   ['Browser', 'Teams', 'OneDrive', 'Mobile', 'API'],
                   [32400, 18700, 15200, 8900, 6400],
                   [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_GREEN, ACCENT_ORANGE, TEXT_DIM])
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Top Active Users",
               ['Email', 'Display Name', 'Total Actions', 'High Risk', 'Suspicious'],
               [['admin@contoso.com', 'Sys Admin', '12,456', '234', '45'],
                ['john.doe@contoso.com', 'John Doe', '8,923', '67', '12'],
                ['external@partner.com', 'Ext Partner', '6,789', '456', '89'],
                ['sara.j@contoso.com', 'Sara Johnson', '5,432', '23', '3'],
                ['api-svc@contoso.com', 'Service Account', '4,567', '12', '0'],
                ['mike.w@contoso.com', 'Mike Wilson', '3,210', '8', '1']])
    fig.savefig(os.path.join(OUTPUT_DIR, '05_user_activity.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 6: Site Security Posture
# ============================================================
def page_06():
    fig = create_figure()
    add_page_title(fig, "Site Security Posture",
                   "Device policies, orphaned sites, and comprehensive security configuration status")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "No Device Policy", "789", ACCENT_ORANGE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Orphaned Sites", "156", ACCENT_RED)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Locked Sites", "34", ACCENT_YELLOW)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Teams Connected", "423", ACCENT_GREEN)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Sites by Risk Tier",
                     ['Critical', 'High', 'Medium', 'Low'],
                     [23, 87, 312, 825],
                     [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "External Sharing Status",
                   ['Enabled', 'Disabled'],
                   [534, 713],
                   [ACCENT_RED, ACCENT_GREEN])
    draw_bar_chart(fig, 0.68, 0.38, 0.30, 0.35, "Device Access Policy",
                   ['Blocked', 'Allowed'],
                   [458, 789],
                   [ACCENT_GREEN, ACCENT_ORANGE])
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Full Site Security Posture",
               ['Site Name', 'Type', 'External', 'Risk Score', 'Tier', 'Device Policy', 'Locked'],
               [['HR Confidential', 'Team', 'Yes', '92', 'Critical', 'No', 'No'],
                ['Finance Portal', 'Communication', 'Yes', '85', 'Critical', 'No', 'No'],
                ['Public Website', 'Communication', 'Yes', '78', 'High', 'Yes', 'No'],
                ['Engineering', 'Team', 'No', '45', 'Medium', 'Yes', 'No'],
                ['CEO OneDrive', 'Personal', 'No', '35', 'Medium', 'Yes', 'No'],
                ['IT Operations', 'Team', 'No', '15', 'Low', 'Yes', 'No']])
    fig.savefig(os.path.join(OUTPUT_DIR, '06_site_security.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 7: Group & Membership Risks
# ============================================================
def page_07():
    fig = create_figure()
    add_page_title(fig, "Group & Membership Risks",
                   "SharePoint groups, ownership gaps, and group-level security risks")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "Security Groups", "234", ACCENT_BLUE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Ownerless Groups", "67", ACCENT_RED)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "M365 Groups", "456", ACCENT_PURPLE)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "High Risk Groups", "89", ACCENT_ORANGE)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Groups by Risk Level",
                     ['Critical', 'High', 'Low'],
                     [23, 66, 811],
                     [ACCENT_RED, ACCENT_ORANGE, ACCENT_GREEN])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Groups by Type",
                   ['SharePointGroup', 'SecurityGroup', 'M365Group'],
                   [456, 234, 210],
                   [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_GREEN])
    draw_bar_chart(fig, 0.68, 0.38, 0.30, 0.35, "Top Groups by Size",
                   ['All Company', 'Engineering', 'Marketing', 'Sales', 'Support'],
                   [4.2, 3.8, 2.9, 2.1, 1.7],
                   [ACCENT_BLUE]*5, horizontal=True)
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Group Risk Details",
               ['Group Name', 'Type', 'Owner Email', 'Owner Name', 'Risk', 'Ownerless'],
               [['External Vendors', 'SecurityGroup', '', '', 'Critical', 'Yes'],
                ['All Company', 'M365Group', '', '', 'High', 'Yes'],
                ['IT Admins', 'SecurityGroup', '', '', 'Critical', 'Yes'],
                ['Marketing Team', 'M365Group', 'mike@contoso.com', 'Mike', 'Low', 'No'],
                ['HR Managers', 'SecurityGroup', 'hr@contoso.com', 'HR Lead', 'Low', 'No'],
                ['Sales Ops', 'SharePointGroup', 'sales@contoso.com', 'Sales Mgr', 'Low', 'No']])
    fig.savefig(os.path.join(OUTPUT_DIR, '07_group_risks.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 8: File Intelligence & Storage
# ============================================================
def page_08():
    fig = create_figure()
    add_page_title(fig, "File Intelligence & Storage",
                   "Version bloat, large files, storage optimization, and file categorization")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "Version Storage (TB)", "4.7", ACCENT_ORANGE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Avg Bloat Ratio", "3.2x", ACCENT_YELLOW)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Large Files (>100MB)", "1,234", ACCENT_RED)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Reclaimable (GB)", "892", ACCENT_GREEN)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Files by Category",
                     ['Documents', 'Spreadsheets', 'Images', 'PDFs', 'Presentations', 'Other'],
                     [145000, 89000, 67000, 52000, 34000, 96000],
                     [ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_RED, ACCENT_ORANGE, TEXT_DIM])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Storage by Site (TB)",
                   ['Engineering', 'Marketing', 'Finance', 'HR', 'Sales'],
                   [3.2, 2.8, 2.1, 1.9, 1.5],
                   [ACCENT_BLUE]*5, horizontal=True)
    draw_bar_chart(fig, 0.68, 0.38, 0.30, 0.35, "Version Bloat by Site",
                   ['Legal Docs', 'Finance', 'Engineering', 'HR', 'Marketing'],
                   [8.5, 6.2, 4.8, 3.1, 2.4],
                   [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN, ACCENT_GREEN],
                   horizontal=True)
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Large & Bloated Files",
               ['File Name', 'Size (MB)', 'Version', 'Bloat Ratio', 'Category', 'Status'],
               [['DB_Backup_Full.bak', '2,450', '45', '12.3x', 'Other', 'Unprotected'],
                ['Video_Training.mp4', '1,890', '3', '1.2x', 'Other', 'Unprotected'],
                ['Design_Assets.zip', '890', '23', '8.7x', 'Other', 'Labeled Only'],
                ['Annual_Report.pptx', '456', '67', '15.2x', 'Presentations', 'Protected'],
                ['Data_Export.xlsx', '345', '12', '4.5x', 'Spreadsheets', 'Unprotected'],
                ['Photo_Archive.zip', '234', '5', '2.1x', 'Other', 'Unprotected']])
    fig.savefig(os.path.join(OUTPUT_DIR, '08_file_intelligence.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 9: Stale Content & Zombie Permissions
# ============================================================
def page_09():
    fig = create_figure()
    add_page_title(fig, "Stale Content & Zombie Permissions",
                   "Inactive files, abandoned sites, and permissions that should have been revoked")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "Stale Files (>180d)", "78,234", ACCENT_ORANGE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Stale Sites (>180d)", "234", ACCENT_ORANGE)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Abandoned (>1yr)", "89", ACCENT_RED)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Zombie Links", "4,567", ACCENT_RED)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "File Age Distribution",
                     ['New (<30d)', 'Recent', 'Standard', 'Old', 'Ancient'],
                     [34000, 67000, 145000, 89000, 148000],
                     [ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_ORANGE, ACCENT_RED])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Stale Files by Site",
                   ['Legacy Portal', 'Old Intranet', 'Archive', 'Dept Share', 'Projects'],
                   [12400, 9800, 8700, 7600, 5400],
                   [ACCENT_RED]*5, horizontal=True)
    draw_donut_chart(fig, 0.68, 0.38, 0.30, 0.35, "Permission Age Distribution",
                     ['New (<30d)', 'Recent', 'Standard', 'Old', 'Ancient'],
                     [5200, 8900, 18000, 12000, 7900],
                     [ACCENT_GREEN, ACCENT_BLUE, ACCENT_YELLOW, ACCENT_ORANGE, ACCENT_RED])
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Zombie Permission Details",
               ['Shared By', 'Link Type', 'Role', 'Age Category', 'Days Old', 'No Expiry'],
               [['former@contoso.com', 'Anyone', 'Write', 'Ancient', '1,245', 'Yes'],
                ['old.vendor@ext.com', 'Anyone', 'Read', 'Ancient', '987', 'Yes'],
                ['ex.emp@contoso.com', 'Specific People', 'Write', 'Old', '623', 'Yes'],
                ['departed@contoso.com', 'Organization', 'Read', 'Old', '534', 'Yes'],
                ['temp@contoso.com', 'Anyone', 'Read', 'Standard', '245', 'Yes'],
                ['intern@contoso.com', 'Specific People', 'Write', 'Standard', '189', 'No']])
    fig.savefig(os.path.join(OUTPUT_DIR, '09_stale_zombie.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)

# ============================================================
# PAGE 10: Risk Scoring & Recommendations
# ============================================================
def page_10():
    fig = create_figure()
    add_page_title(fig, "Risk Scoring & Recommendations",
                   "Composite risk analysis, scoring breakdown, and prioritized remediation actions")
    draw_card(fig, 0.02, 0.76, 0.22, 0.13, "Composite Risk Index", "62", ACCENT_ORANGE)
    draw_card(fig, 0.26, 0.76, 0.22, 0.13, "Data Exposure Score", "45", ACCENT_YELLOW)
    draw_card(fig, 0.50, 0.76, 0.22, 0.13, "Risk Reduction Items", "347", ACCENT_GREEN)
    draw_card(fig, 0.74, 0.76, 0.24, 0.13, "Sites Above Threshold", "110", ACCENT_RED)
    draw_donut_chart(fig, 0.02, 0.38, 0.30, 0.35, "Site Risk Tier Distribution",
                     ['Critical', 'High', 'Medium', 'Low'],
                     [23, 87, 312, 825],
                     [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN])
    draw_bar_chart(fig, 0.35, 0.38, 0.30, 0.35, "Average Risk by Tier",
                   ['Critical', 'High', 'Medium', 'Low'],
                   [88, 67, 42, 18],
                   [ACCENT_RED, ACCENT_ORANGE, ACCENT_YELLOW, ACCENT_GREEN])
    draw_bar_chart(fig, 0.68, 0.38, 0.30, 0.35, "Risk Score by Site Type",
                   ['Team', 'Communication', 'Personal'],
                   [52, 38, 24],
                   [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_GREEN])
    draw_table(fig, 0.02, 0.02, 0.96, 0.33, "Top 25 Highest Risk Sites",
               ['Site Name', 'Type', 'Risk Score', 'Tier', 'External', 'Labeled', 'Orphaned'],
               [['HR Confidential', 'Team', '92', 'Critical', 'Yes', 'No', 'Yes'],
                ['Finance Shared', 'Team', '88', 'Critical', 'Yes', 'No', 'No'],
                ['Executive Board', 'Comm.', '85', 'Critical', 'Yes', 'No', 'Yes'],
                ['Sales External', 'Team', '78', 'High', 'Yes', 'Yes', 'No'],
                ['Legal Archive', 'Team', '75', 'High', 'No', 'No', 'Yes'],
                ['Marketing Hub', 'Comm.', '72', 'High', 'Yes', 'Yes', 'No']])
    fig.savefig(os.path.join(OUTPUT_DIR, '10_risk_recommendations.png'),
                facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    print("Generating dashboard mockups...")
    pages = [page_01, page_02, page_03, page_04, page_05,
             page_06, page_07, page_08, page_09, page_10]
    for i, page_fn in enumerate(pages, 1):
        print(f"  Page {i}/10: {page_fn.__name__}...")
        page_fn()
    print(f"\nDone! {len(pages)} mockups saved to {OUTPUT_DIR}/")
