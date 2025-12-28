"""
LawTrax Marketing Command Center
A comprehensive marketing platform for SEO, content generation, and lead generation
Built for immigration software marketing teams
"""

import streamlit as st
import anthropic
from datetime import datetime
import json
import re

# Page Configuration
st.set_page_config(
    page_title="Marketing Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4B0082;
        --secondary-color: #7B68EE;
        --accent-color: #9370DB;
        --success-color: #32CD32;
        --warning-color: #FFA500;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #4B0082;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    .linkedin-badge { background: #0077B5; color: white; }
    .instagram-badge { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }
    .tiktok-badge { background: #000000; color: white; }
    .youtube-badge { background: #FF0000; color: white; }
    .twitter-badge { background: #1DA1F2; color: white; }
    .facebook-badge { background: #4267B2; color: white; }
    
    /* Content output styling */
    .content-output {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-top: 1rem;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4B0082;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(75, 0, 130, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []
if 'company_profile' not in st.session_state:
    st.session_state.company_profile = {}
if 'api_key' not in st.session_state:
    # Try to get API key from Streamlit secrets first
    try:
        st.session_state.api_key = st.secrets.get("CLAUDE_API_KEY", "") or st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        st.session_state.api_key = ""

# Company Knowledge Base (Default: LawTrax)
LAWTRAX_KNOWLEDGE = """
COMPANY: LawTrax
TAGLINE: "Immigration Software for the Modern Attorney"
WEBSITE: lawtrax.com

CORE VALUE PROPOSITION:
LawTrax is a secure, cloud-based immigration case management platform that empowers attorney firms to manage leads, clients, and cases effortlessly. The platform enables customizable workflows, seamless carrier label generation, and integrated invoice management.

KEY FEATURES:
1. Case Management - Workflow-based platform with multiple stages based on case type, enabling end-to-end management, tracking, and stakeholder notifications
2. Customer Management - Secure cloud portal for companies/beneficiaries to manage information and initiate cases with single-click automation
3. Lead Management - Built-in CRM for converting prospects to customers with lead categorization and tracking
4. Document Management - Cloud-based, indexable, searchable system with three stages: identification, generation, and delivery
5. Dashboard Reporting - Real-time business-driven dashboards with drill-down capabilities and configurable KPIs
6. PDF Generation - Auto-generates USCIS/DoL formatted documents based on case type rules
7. Client Portal - Secure document uploads and case status tracking with automated notifications
8. Integration Capabilities - Outlook calendar, QuickBooks billing, webhooks, and RESTful APIs

SECURITY & COMPLIANCE:
- Multi-tenant architecture on Google Cloud Platform with Firebase
- SOC 2 Type II certification (in pipeline)
- GDPR compliance (in pipeline)
- HIPAA compliant architecture
- End-to-end encryption for data at rest and in transit
- Role-based access control with SSO support
- California Consumer Privacy Act (CCPA) compliance
- PCI compliance with digital tokens for authentication

TECHNICAL SPECIFICATIONS:
- Cloud-hosted on Google Cloud Platform
- Multi-tenant SaaS with broker patterns for tenant isolation
- RESTful APIs with no additional costs
- Real-time reporting (no batch delays)
- 99.9% uptime guarantee on Google infrastructure
- Automatic OCR capabilities
- Real-time form updates from USCIS

KEY DIFFERENTIATORS:
1. No additional API costs (unlike competitors)
2. True real-time reporting without 24-hour batch delays
3. Guaranteed uptime on Google's enterprise infrastructure
4. Built-in PDF generator for USCIS/DoL formatted submissions
5. Comprehensive audit trail for all document actions
6. Customizable email templates and notification engine

CLIENT SUCCESS METRICS:
- Clients report 30%+ revenue increase
- Reduced administrative burden
- Faster case completion through digital automation
- Increased capacity for new clients

TARGET MARKET:
- Immigration law firms (solo to enterprise)
- Corporate immigration departments
- Global mobility teams
- Legal service providers

CONTACT:
- Email: info@lawtrax.com
- Phone: 972-200-1030
- Address: 17400 Dallas Parkway, Suite 121, Dallas, Texas 75287
"""

# Platform-specific content guidelines
PLATFORM_GUIDELINES = {
    "LinkedIn": {
        "max_chars": 3000,
        "hashtags": 3,
        "tone": "Professional, thought leadership focused",
        "format": "Long-form posts, articles, carousel documents",
        "best_practices": [
            "Start with a hook in the first 2 lines",
            "Use line breaks for readability",
            "Include a clear call-to-action",
            "Tag relevant people/companies",
            "Post during business hours (Tue-Thu optimal)",
            "Use 3-5 relevant hashtags at the end"
        ],
        "content_types": ["Thought leadership", "Industry insights", "Case studies", "Company updates", "Employee spotlights", "How-to guides"]
    },
    "Instagram": {
        "max_chars": 2200,
        "hashtags": 20,
        "tone": "Visual, engaging, authentic",
        "format": "Carousel posts, Reels, Stories, Feed posts",
        "best_practices": [
            "Lead with value in the first line",
            "Use emojis strategically",
            "Include save-worthy content",
            "Create shareable graphics",
            "Use Instagram-specific features (polls, questions)",
            "Post 1-2 times daily for optimal reach"
        ],
        "content_types": ["Educational carousels", "Behind-the-scenes", "Client testimonials", "Quick tips", "Infographics", "Day-in-the-life"]
    },
    "TikTok": {
        "max_chars": 300,
        "hashtags": 5,
        "tone": "Casual, entertaining, educational",
        "format": "Short-form video (15-60 seconds optimal)",
        "best_practices": [
            "Hook viewers in the first 3 seconds",
            "Use trending sounds and effects",
            "Keep it authentic and relatable",
            "Add captions for accessibility",
            "End with a question or CTA",
            "Post 1-3 times daily"
        ],
        "content_types": ["Quick tips", "Myth-busting", "Day-in-the-life", "Trending challenges", "Educational content", "Q&A responses"]
    },
    "YouTube": {
        "max_chars": 5000,
        "hashtags": 3,
        "tone": "Educational, authoritative, engaging",
        "format": "Long-form videos, Shorts, tutorials",
        "best_practices": [
            "Optimize title with keywords",
            "Create compelling thumbnails",
            "Include timestamps for long videos",
            "Add end screens and cards",
            "Write detailed descriptions with keywords",
            "Engage with comments"
        ],
        "content_types": ["Tutorials", "Case studies", "Webinars", "Product demos", "Expert interviews", "Industry updates"]
    },
    "Twitter/X": {
        "max_chars": 280,
        "hashtags": 2,
        "tone": "Conversational, timely, engaging",
        "format": "Threads, single tweets, polls",
        "best_practices": [
            "Keep tweets concise and punchy",
            "Use threads for longer content",
            "Engage with trending topics",
            "Reply to relevant conversations",
            "Use polls for engagement",
            "Post multiple times daily"
        ],
        "content_types": ["Quick insights", "Industry news commentary", "Threads", "Polls", "Quotes", "Live event coverage"]
    },
    "Facebook": {
        "max_chars": 63206,
        "hashtags": 3,
        "tone": "Community-focused, informative, personable",
        "format": "Posts, videos, events, groups",
        "best_practices": [
            "Create shareable content",
            "Use Facebook Live for engagement",
            "Build and engage with groups",
            "Post native video content",
            "Use Facebook Events for webinars",
            "Respond to comments promptly"
        ],
        "content_types": ["Community updates", "Live videos", "Event promotions", "Educational posts", "Client stories", "Behind-the-scenes"]
    }
}

# Content types and templates
CONTENT_TYPES = {
    "Educational Post": "Create informative content that educates the audience about immigration processes, software benefits, or industry trends",
    "Success Story": "Share client success stories and testimonials that demonstrate value",
    "Product Feature Spotlight": "Highlight specific features and their benefits",
    "Industry News Commentary": "Provide expert commentary on immigration law updates",
    "Tips & Best Practices": "Share actionable tips for immigration professionals",
    "Behind-the-Scenes": "Show company culture, team, and development process",
    "Comparison Post": "Compare solutions or approaches in the market",
    "FAQ Content": "Address common questions and concerns",
    "Announcement": "Share company news, updates, or launches",
    "Engagement Post": "Create interactive content to boost engagement"
}

def get_claude_response(prompt, api_key):
    """Generate content using Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "ERROR: Invalid API key. Please check your Claude API key."
    except anthropic.RateLimitError:
        return "ERROR: Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"ERROR: {str(e)}"

def build_content_prompt(company_info, platform, content_type, topic, additional_context, tone, target_audience):
    """Build a comprehensive prompt for content generation"""
    guidelines = PLATFORM_GUIDELINES.get(platform, PLATFORM_GUIDELINES["LinkedIn"])
    
    prompt = f"""You are an expert social media content strategist and copywriter specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

PLATFORM: {platform}
CONTENT TYPE: {content_type}
TOPIC/THEME: {topic}

PLATFORM SPECIFICATIONS:
- Maximum Characters: {guidelines['max_chars']}
- Recommended Hashtags: {guidelines['hashtags']}
- Tone: {guidelines['tone']}
- Format: {guidelines['format']}

BEST PRACTICES FOR {platform.upper()}:
{chr(10).join(['- ' + bp for bp in guidelines['best_practices']])}

TARGET AUDIENCE: {target_audience}
DESIRED TONE: {tone}

ADDITIONAL CONTEXT/REQUIREMENTS:
{additional_context if additional_context else 'None specified'}

TASK:
Create a compelling {content_type.lower()} for {platform} about "{topic}".

The content should:
1. Be optimized for {platform}'s algorithm and best practices
2. Include a strong hook/opening
3. Provide genuine value to the target audience
4. Include a clear call-to-action
5. Be formatted appropriately for the platform
6. Include relevant hashtags (exact number: {guidelines['hashtags']})
7. Stay within character limits

OUTPUT FORMAT:
Provide the ready-to-post content with:
1. MAIN CONTENT (the actual post text)
2. HASHTAGS (platform-appropriate)
3. POSTING TIPS (2-3 specific tips for this post)
4. BEST TIME TO POST (recommended timing)
5. SUGGESTED VISUAL (description of ideal accompanying image/video)

Make the content engaging, authentic, and aligned with the company's voice while following all platform best practices."""

    return prompt

def build_video_script_prompt(company_info, platform, video_type, topic, duration, additional_context):
    """Build prompt for video script generation"""
    prompt = f"""You are an expert video content strategist and scriptwriter specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

PLATFORM: {platform}
VIDEO TYPE: {video_type}
TOPIC: {topic}
TARGET DURATION: {duration}

ADDITIONAL CONTEXT:
{additional_context if additional_context else 'None specified'}

TASK:
Create a complete video script for a {video_type} about "{topic}" for {platform}.

The script should include:

1. HOOK (First 3 seconds) - Attention-grabbing opening
2. INTRO (5-10 seconds) - Brief context setting
3. MAIN CONTENT - Structured body with clear sections
4. CALL TO ACTION - What viewers should do next
5. OUTRO - Memorable closing

OUTPUT FORMAT:
Provide a complete script with:
1. FULL SCRIPT (with timestamps and speaker directions)
2. B-ROLL SUGGESTIONS (visual elements to include)
3. ON-SCREEN TEXT/GRAPHICS (key points to display)
4. MUSIC/SOUND RECOMMENDATIONS
5. THUMBNAIL CONCEPT (for YouTube/TikTok)
6. CAPTION/DESCRIPTION (for posting)
7. HASHTAGS (platform-appropriate)

Make it engaging, informative, and optimized for {platform}'s algorithm."""

    return prompt

def build_seo_content_prompt(company_info, content_type, primary_keyword, secondary_keywords, target_word_count, additional_context):
    """Build prompt for SEO-optimized content"""
    prompt = f"""You are an expert SEO content strategist and writer specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

CONTENT TYPE: {content_type}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET WORD COUNT: {target_word_count}

ADDITIONAL CONTEXT:
{additional_context if additional_context else 'None specified'}

TASK:
Create SEO-optimized content for "{primary_keyword}".

The content should:
1. Naturally incorporate the primary keyword in title, headers, and body
2. Include secondary keywords throughout
3. Follow on-page SEO best practices
4. Provide genuine value to readers
5. Include internal linking opportunities
6. Be structured with proper H1, H2, H3 hierarchy

OUTPUT FORMAT:
Provide complete content with:
1. META TITLE (50-60 characters)
2. META DESCRIPTION (150-160 characters)
3. FULL CONTENT (with proper heading structure)
4. KEYWORD DENSITY ANALYSIS
5. INTERNAL LINKING SUGGESTIONS
6. FEATURED SNIPPET OPTIMIZATION (structured for position zero)
7. FAQ SECTION (for additional keyword targeting)
8. SCHEMA MARKUP SUGGESTIONS

Make it comprehensive, authoritative, and optimized for search intent."""

    return prompt

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🚀 Marketing Command Center</h2>
        <p>Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Input
    st.markdown("### 🔑 API Configuration")
    
    # Check if API key is already loaded from secrets
    if st.session_state.api_key:
        st.success("✅ API Key loaded from secrets")
        # Option to override
        override_key = st.checkbox("Override API Key", value=False)
        if override_key:
            api_key = st.text_input(
                "Enter New API Key",
                type="password",
                help="Enter your Anthropic Claude API key to override"
            )
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ API Key updated")
    else:
        api_key = st.text_input(
            "Claude API Key",
            type="password",
            value="",
            help="Enter your Anthropic Claude API key (or add CLAUDE_API_KEY to secrets.toml)"
        )
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Add CLAUDE_API_KEY to secrets.toml or enter below")
    
    st.divider()
    
    # Company Configuration
    st.markdown("### 🏢 Company Profile")
    use_default = st.checkbox("Use LawTrax (Default)", value=True)
    
    if not use_default:
        company_name = st.text_input("Company Name", placeholder="Enter company name")
        company_description = st.text_area(
            "Company Description",
            placeholder="Describe your company, products, and value proposition...",
            height=150
        )
        company_website = st.text_input("Website", placeholder="https://example.com")
        target_market = st.text_input("Target Market", placeholder="e.g., Immigration law firms")
        key_features = st.text_area(
            "Key Features/Benefits",
            placeholder="List your main features and benefits...",
            height=100
        )
        
        if company_name and company_description:
            st.session_state.company_profile = {
                "name": company_name,
                "description": company_description,
                "website": company_website,
                "target_market": target_market,
                "features": key_features
            }
    
    st.divider()
    
    # Quick Stats
    st.markdown("### 📊 Session Stats")
    st.metric("Content Generated", len(st.session_state.generated_content))
    
    if st.button("🗑️ Clear History"):
        st.session_state.generated_content = []
        st.rerun()

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Marketing Command Center</h1>
    <p>AI-Powered Content Generation for Immigration Software Marketing</p>
</div>
""", unsafe_allow_html=True)

# Get company info
if use_default:
    company_info = LAWTRAX_KNOWLEDGE
    company_display_name = "LawTrax"
else:
    if st.session_state.company_profile:
        profile = st.session_state.company_profile
        company_info = f"""
COMPANY: {profile.get('name', 'N/A')}
WEBSITE: {profile.get('website', 'N/A')}
DESCRIPTION: {profile.get('description', 'N/A')}
TARGET MARKET: {profile.get('target_market', 'N/A')}
KEY FEATURES: {profile.get('features', 'N/A')}
"""
        company_display_name = profile.get('name', 'Your Company')
    else:
        company_info = "No company profile configured. Please set up in sidebar."
        company_display_name = "Your Company"

# Main Tabs
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 LawTrax Overview",
    "📱 Social Media Content",
    "🎬 Video Scripts",
    "🔍 SEO Content",
    "📚 Knowledge Base",
    "📋 Content History"
])

# Tab 0: LawTrax Overview (Landing Page)
with tab0:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #4B0082; font-size: 3rem; margin-bottom: 0;">LAWTRAX</h1>
        <p style="font-size: 1.5rem; color: #666; margin-top: 0;">Immigration Software for the Modern Attorney</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4B0082 0%, #7B68EE 50%, #9370DB 100%); 
                padding: 2.5rem; border-radius: 20px; color: white; margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(75, 0, 130, 0.3);">
        <h2 style="margin-bottom: 1rem; font-size: 1.8rem;">🚀 The Only Cloud-Based Digital Attorney Platform You Need</h2>
        <p style="font-size: 1.1rem; line-height: 1.8; opacity: 0.95;">
            LawTrax empowers immigration attorney firms with a secure, all-in-one platform to manage leads, clients, 
            and cases effortlessly. Customize workflows to fit your business needs, seamlessly integrate carrier label 
            generation and invoice management, and maximize efficiency with our streamlined solution.
        </p>
        <div style="margin-top: 1.5rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ 30%+ Revenue Increase</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ 99.9% Uptime</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ Real-Time Reporting</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ Zero API Costs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("### 📊 Platform Impact")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Revenue Increase", "30%+", "Client Reported")
    with metric_col2:
        st.metric("Platform Uptime", "99.9%", "Google Cloud")
    with metric_col3:
        st.metric("Report Delay", "0 hrs", "vs 24hr industry avg")
    with metric_col4:
        st.metric("API Cost", "$0", "Included Free")
    
    st.markdown("---")
    
    # Core Platform Features
    st.markdown("### 🎯 Core Platform Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #4B0082; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #4B0082; margin-bottom: 0.5rem;">📋 Case Management</h4>
            <p style="color: #555; margin: 0;">Workflow-based platform with multiple stages based on case type. 
            End-to-end management, tracking, assigning, and real-time stakeholder notifications. 
            Business rules ensure all required documents are captured and verified before completion.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #7B68EE; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #7B68EE; margin-bottom: 0.5rem;">👥 Customer Management</h4>
            <p style="color: #555; margin: 0;">Secure cloud portal for companies and beneficiaries to manage 
            information and initiate cases with a single click. Complete automation from attorney assignment 
            to case completion based on provided data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #9370DB; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #9370DB; margin-bottom: 0.5rem;">🎯 Lead Management</h4>
            <p style="color: #555; margin: 0;">Built-in CRM to convert prospects into customers. Track leads 
            at various conversion stages with recorded interactions. Categorize as potential or hot leads 
            with dedicated team assignment for tracking and closure.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #32CD32; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #32CD32; margin-bottom: 0.5rem;">📄 Document Management</h4>
            <p style="color: #555; margin: 0;">Cloud-based, indexable, searchable system with three stages: 
            identification, generation, and delivery. Documents merged into single PDF per visa type. 
            Complete audit trail for all uploads, edits, assignments, and deletions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #FF6B6B; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #FF6B6B; margin-bottom: 0.5rem;">📊 Dashboard & Reporting</h4>
            <p style="color: #555; margin: 0;">Real-time business-driven dashboards with drill-down capabilities. 
            Configurable KPIs with drag-and-drop functionality. Comprehensive reporting for decision-making 
            with customizable branded reports.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #4ECDC4; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #4ECDC4; margin-bottom: 0.5rem;">📝 PDF Generation</h4>
            <p style="color: #555; margin: 0;">Auto-generate USCIS and DoL formatted documents based on case type rules. 
            Identifies case type, collates required data, and generates submission-ready documents 
            following all visa-specific conditions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #FFE66D; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #E6B800; margin-bottom: 0.5rem;">🌐 Client Portal</h4>
            <p style="color: #555; margin: 0;">Secure document uploads and case status tracking for clients. 
            Automated notifications on case updates. Exclusive cloud portal for companies to manage 
            information and initiate beneficiary cases.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #96CEB4; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #96CEB4; margin-bottom: 0.5rem;">🔗 Integrations</h4>
            <p style="color: #555; margin: 0;">Outlook integration for meetings, appointments, and case alerts. 
            QuickBooks billing system integration. Webhooks and RESTful APIs for third-party integrations 
            with no additional costs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Security & Compliance
    st.markdown("### 🔒 Enterprise Security & Compliance")
    
    sec_col1, sec_col2, sec_col3 = st.columns(3)
    
    with sec_col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛡️</div>
            <h4 style="color: #4B0082;">Infrastructure Security</h4>
            <p style="color: #666; font-size: 0.9rem;">
                Multi-tenant SaaS on Google Cloud Platform with Firebase. 
                Broker patterns for tenant isolation. 99.9% uptime guarantee.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with sec_col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔐</div>
            <h4 style="color: #4B0082;">Data Protection</h4>
            <p style="color: #666; font-size: 0.9rem;">
                End-to-end encryption at rest and in transit. Each client has own instance. 
                Digital tokens for API authentication.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with sec_col3:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
            <h4 style="color: #4B0082;">Compliance Ready</h4>
            <p style="color: #666; font-size: 0.9rem;">
                SOC 2 Type II • GDPR • HIPAA Compliant • CCPA • PCI Compliance • 
                Role-based access with SSO support.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Competitive Advantages
    st.markdown("### 💪 Why Choose LawTrax Over Competitors?")
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4CAF50;">
            <h4 style="color: #2E7D32; margin: 0 0 0.5rem 0;">✅ No Additional API Costs</h4>
            <p style="margin: 0; color: #555;">Unlike competitors who charge extra for API access, 
            LawTrax includes full API capabilities at no additional cost.</p>
        </div>
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #2196F3;">
            <h4 style="color: #1565C0; margin: 0 0 0.5rem 0;">✅ True Real-Time Reporting</h4>
            <p style="margin: 0; color: #555;">No 24-hour batch delays. Get instant access to your data 
            when you need it for client support and decision making.</p>
        </div>
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FF9800;">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0;">✅ Google Cloud Infrastructure</h4>
            <p style="margin: 0; color: #555;">Enterprise-grade 99.9% uptime guarantee backed by 
            Google's world-class infrastructure and security.</p>
        </div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #9C27B0;">
            <h4 style="color: #7B1FA2; margin: 0 0 0.5rem 0;">✅ Built-in USCIS/DoL Generator</h4>
            <p style="margin: 0; color: #555;">Automatic PDF generation in proper government format 
            with business rules for each visa type.</p>
        </div>
        <div style="background: #ffebee; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f44336;">
            <h4 style="color: #C62828; margin: 0 0 0.5rem 0;">✅ Complete Audit Trail</h4>
            <p style="margin: 0; color: #555;">Every action is logged for compliance. Know who did what 
            and when across every case and document.</p>
        </div>
        <div style="background: #e0f7fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #00BCD4;">
            <h4 style="color: #00838F; margin: 0 0 0.5rem 0;">✅ 25+ Years Experience</h4>
            <p style="margin: 0; color: #555;">Built by experts with collective 25+ years in immigration 
            law technology and digital processing.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Target Market
    st.markdown("### 🎯 Who Uses LawTrax?")
    
    market_col1, market_col2, market_col3, market_col4 = st.columns(4)
    
    with market_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">⚖️</div>
            <h4 style="color: #4B0082;">Immigration Law Firms</h4>
            <p style="color: #666; font-size: 0.85rem;">Solo practitioners to large enterprises</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🏢</div>
            <h4 style="color: #4B0082;">Corporate Immigration</h4>
            <p style="color: #666; font-size: 0.85rem;">In-house immigration departments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🌍</div>
            <h4 style="color: #4B0082;">Global Mobility Teams</h4>
            <p style="color: #666; font-size: 0.85rem;">International workforce management</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🤝</div>
            <h4 style="color: #4B0082;">Legal Service Providers</h4>
            <p style="color: #666; font-size: 0.85rem;">Immigration-focused legal services</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Client Testimonial
    st.markdown("### 💬 Client Success Story")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <div style="font-size: 3rem; opacity: 0.3; margin-bottom: -1rem;">❝</div>
        <p style="font-size: 1.2rem; line-height: 1.8; font-style: italic;">
            "LawTrax has helped us put the customer's interests first and focus on cases and interactions 
            rather than operations and paperwork. We realized that we could handle more cases than we were 
            managing, resulting in an <strong>increase in our revenue of at least 30%</strong>. I highly recommend 
            this tool for attorneys and firms looking to improve productivity."
        </p>
        <p style="margin-top: 1rem; font-weight: bold;">— Immigration Law Firm Client</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact Information
    st.markdown("### 📞 Get Started with LawTrax")
    
    contact_col1, contact_col2, contact_col3 = st.columns(3)
    
    with contact_col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">📧</div>
            <h4>Email Us</h4>
            <p style="color: #4B0082; font-weight: bold;">info@lawtrax.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">📱</div>
            <h4>Call Us</h4>
            <p style="color: #4B0082; font-weight: bold;">972-200-1030</p>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">🌐</div>
            <h4>Visit Website</h4>
            <p style="color: #4B0082; font-weight: bold;">lawtrax.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; color: #666;">
        <p>📍 17400 Dallas Parkway, Suite 121, Dallas, Texas 75287</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">Ready to Transform Your Immigration Practice?</h3>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem;">
            Use the tabs above to generate marketing content, or visit lawtrax.com to schedule a demo!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 1: Social Media Content
with tab1:
    st.markdown("## 📱 Social Media Content Generator")
    st.markdown(f"Creating content for **{company_display_name}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Select Platform",
            list(PLATFORM_GUIDELINES.keys()),
            help="Choose the social media platform"
        )
        
        content_type = st.selectbox(
            "Content Type",
            list(CONTENT_TYPES.keys()),
            help="Select the type of content to create"
        )
        
        topic = st.text_input(
            "Topic/Theme",
            placeholder="e.g., Benefits of cloud-based case management",
            help="What should the post be about?"
        )
    
    with col2:
        target_audience = st.text_input(
            "Target Audience",
            value="Immigration attorneys, law firm partners, and legal operations managers",
            help="Who is this content for?"
        )
        
        tone = st.selectbox(
            "Tone",
            ["Professional", "Conversational", "Educational", "Inspiring", "Urgent", "Friendly", "Authoritative"],
            help="Select the desired tone"
        )
        
        additional_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Any specific points to include, avoid, or emphasize...",
            height=100
        )
    
    # Platform-specific info
    guidelines = PLATFORM_GUIDELINES.get(platform, {})
    st.markdown(f"""
    <div class="info-box">
        <strong>📌 {platform} Guidelines:</strong><br>
        • Max Characters: {guidelines.get('max_chars', 'N/A')}<br>
        • Recommended Hashtags: {guidelines.get('hashtags', 'N/A')}<br>
        • Tone: {guidelines.get('tone', 'N/A')}<br>
        • Best Formats: {guidelines.get('format', 'N/A')}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✨ Generate Social Media Content", type="primary", use_container_width=True):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not topic:
            st.error("⚠️ Please enter a topic")
        else:
            with st.spinner(f"🎨 Creating {platform} content..."):
                prompt = build_content_prompt(
                    company_info, platform, content_type, topic,
                    additional_context, tone, target_audience
                )
                result = get_claude_response(prompt, st.session_state.api_key)
                
                if not result.startswith("ERROR"):
                    st.session_state.generated_content.append({
                        "type": "Social Media",
                        "platform": platform,
                        "topic": topic,
                        "content": result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.markdown('<div class="success-banner">✅ Content Generated Successfully!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Generated Content")
                    st.markdown(result)
                    
                    # Copy button
                    st.download_button(
                        label="📥 Download Content",
                        data=result,
                        file_name=f"{platform.lower()}_{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(result)

# Tab 2: Video Scripts
with tab2:
    st.markdown("## 🎬 Video Script Generator")
    st.markdown(f"Creating video content for **{company_display_name}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_platform = st.selectbox(
            "Platform",
            ["TikTok", "YouTube", "Instagram Reels", "LinkedIn Video", "Facebook Video"],
            key="video_platform"
        )
        
        video_type = st.selectbox(
            "Video Type",
            [
                "Product Demo",
                "Educational/How-To",
                "Testimonial/Case Study",
                "Industry Tips",
                "Behind-the-Scenes",
                "FAQ/Q&A",
                "Announcement/News",
                "Comparison",
                "Day-in-the-Life",
                "Trending Challenge Adaptation"
            ]
        )
        
        video_topic = st.text_input(
            "Video Topic",
            placeholder="e.g., 5 ways to streamline H-1B processing",
            key="video_topic"
        )
    
    with col2:
        duration = st.selectbox(
            "Target Duration",
            ["15 seconds (TikTok/Reels)", "30 seconds", "60 seconds", "2-3 minutes", "5-10 minutes (YouTube)", "10+ minutes (Deep Dive)"]
        )
        
        video_style = st.selectbox(
            "Style",
            ["Talking Head", "Screen Recording", "Animation", "Mixed Media", "Documentary", "Vlog"]
        )
        
        video_context = st.text_area(
            "Additional Requirements",
            placeholder="Specific points, target audience, or special requirements...",
            height=100,
            key="video_context"
        )
    
    if st.button("🎥 Generate Video Script", type="primary", use_container_width=True):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not video_topic:
            st.error("⚠️ Please enter a video topic")
        else:
            with st.spinner("🎬 Creating video script..."):
                prompt = build_video_script_prompt(
                    company_info, video_platform, video_type,
                    video_topic, duration, video_context
                )
                result = get_claude_response(prompt, st.session_state.api_key)
                
                if not result.startswith("ERROR"):
                    st.session_state.generated_content.append({
                        "type": "Video Script",
                        "platform": video_platform,
                        "topic": video_topic,
                        "content": result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.markdown('<div class="success-banner">✅ Video Script Generated!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Generated Script")
                    st.markdown(result)
                    
                    st.download_button(
                        label="📥 Download Script",
                        data=result,
                        file_name=f"video_script_{video_platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(result)

# Tab 3: SEO Content
with tab3:
    st.markdown("## 🔍 SEO Content Generator")
    st.markdown(f"Creating SEO-optimized content for **{company_display_name}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        seo_content_type = st.selectbox(
            "Content Type",
            [
                "Blog Post",
                "Landing Page",
                "Product Page",
                "Service Page",
                "Comparison Article",
                "How-To Guide",
                "Listicle",
                "Case Study",
                "Industry Report",
                "FAQ Page"
            ],
            key="seo_content_type"
        )
        
        primary_keyword = st.text_input(
            "Primary Keyword",
            placeholder="e.g., immigration case management software",
            help="Main keyword to target"
        )
        
        secondary_keywords = st.text_area(
            "Secondary Keywords",
            placeholder="immigration software, law firm case management, USCIS forms automation",
            help="Additional keywords to include (one per line or comma-separated)",
            height=100
        )
    
    with col2:
        target_word_count = st.select_slider(
            "Target Word Count",
            options=[500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000],
            value=1500
        )
        
        search_intent = st.selectbox(
            "Search Intent",
            ["Informational", "Commercial", "Transactional", "Navigational"]
        )
        
        seo_context = st.text_area(
            "Additional Requirements",
            placeholder="Specific angle, competitor analysis, target audience...",
            height=100,
            key="seo_context"
        )
    
    # SEO Tips
    st.markdown("""
    <div class="info-box">
        <strong>📌 SEO Best Practices:</strong><br>
        • Include primary keyword in title, first paragraph, and H2s<br>
        • Use secondary keywords naturally throughout<br>
        • Aim for 2-3% keyword density<br>
        • Include internal and external links<br>
        • Optimize for featured snippets with clear answers
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Generate SEO Content", type="primary", use_container_width=True):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not primary_keyword:
            st.error("⚠️ Please enter a primary keyword")
        else:
            with st.spinner("📝 Creating SEO-optimized content..."):
                prompt = build_seo_content_prompt(
                    company_info, seo_content_type, primary_keyword,
                    secondary_keywords, target_word_count, seo_context
                )
                result = get_claude_response(prompt, st.session_state.api_key)
                
                if not result.startswith("ERROR"):
                    st.session_state.generated_content.append({
                        "type": "SEO Content",
                        "platform": "Website/Blog",
                        "topic": primary_keyword,
                        "content": result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.markdown('<div class="success-banner">✅ SEO Content Generated!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Generated Content")
                    st.markdown(result)
                    
                    st.download_button(
                        label="📥 Download Content",
                        data=result,
                        file_name=f"seo_{seo_content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(result)

# Tab 4: Knowledge Base
with tab4:
    st.markdown("## 📚 Company Knowledge Base")
    
    if use_default:
        st.markdown("### LawTrax - Immigration Case Management Software")
        
        # Key Features Section
        st.markdown("#### 🎯 Key Features")
        features = [
            ("Case Management", "Workflow-based platform with multiple stages based on case type"),
            ("Customer Management", "Secure cloud portal for companies and beneficiaries"),
            ("Lead Management", "Built-in CRM for converting prospects to customers"),
            ("Document Management", "Cloud-based, indexable, searchable document system"),
            ("Dashboard Reporting", "Real-time business-driven dashboards with drill-down"),
            ("PDF Generation", "Auto-generates USCIS/DoL formatted documents"),
            ("Client Portal", "Secure uploads and case tracking with notifications"),
            ("Integrations", "Outlook, QuickBooks, webhooks, and RESTful APIs")
        ]
        
        cols = st.columns(2)
        for i, (feature, desc) in enumerate(features):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="feature-card">
                    <strong>{feature}</strong><br>
                    <small>{desc}</small>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
        
        # Competitive Advantages
        st.markdown("#### 💪 Competitive Advantages")
        advantages = [
            "✅ No additional API costs (unlike competitors)",
            "✅ True real-time reporting (no 24-hour batch delays)",
            "✅ 99.9% uptime on Google Cloud infrastructure",
            "✅ Built-in USCIS/DoL PDF generator",
            "✅ Complete audit trail for compliance",
            "✅ 30%+ revenue increase reported by clients"
        ]
        for adv in advantages:
            st.markdown(adv)
        
        # Target Market
        st.markdown("#### 🎯 Target Market")
        targets = ["Immigration law firms (solo to enterprise)", "Corporate immigration departments", 
                   "Global mobility teams", "Legal service providers"]
        st.markdown(" | ".join(targets))
        
        # Content Inspiration
        st.markdown("#### 💡 Content Topic Ideas")
        topics = {
            "Educational": [
                "How to streamline H-1B processing with case management software",
                "5 signs your law firm needs to upgrade immigration software",
                "The complete guide to USCIS form automation",
                "Why real-time reporting matters for immigration law firms"
            ],
            "Thought Leadership": [
                "The future of immigration law technology",
                "How AI is transforming immigration case management",
                "Cloud security best practices for law firms",
                "Building a scalable immigration practice"
            ],
            "Client Success": [
                "How [Client] increased revenue 30% with LawTrax",
                "Case study: Reducing administrative burden in immigration law",
                "From manual to automated: A law firm's digital transformation"
            ],
            "Product": [
                "Introducing our new client portal features",
                "How our document management saves 10+ hours weekly",
                "Behind the scenes: How we ensure 99.9% uptime"
            ]
        }
        
        for category, ideas in topics.items():
            with st.expander(f"📌 {category} Topics"):
                for idea in ideas:
                    st.markdown(f"• {idea}")
    else:
        if st.session_state.company_profile:
            profile = st.session_state.company_profile
            st.markdown(f"### {profile.get('name', 'Your Company')}")
            st.markdown(f"**Website:** {profile.get('website', 'Not specified')}")
            st.markdown(f"**Target Market:** {profile.get('target_market', 'Not specified')}")
            st.markdown("#### Description")
            st.markdown(profile.get('description', 'No description provided'))
            st.markdown("#### Key Features")
            st.markdown(profile.get('features', 'No features listed'))
        else:
            st.warning("⚠️ Please configure your company profile in the sidebar")

# Tab 5: Content History
with tab5:
    st.markdown("## 📋 Content History")
    
    if st.session_state.generated_content:
        for i, item in enumerate(reversed(st.session_state.generated_content)):
            with st.expander(f"📄 {item['type']} - {item['platform']} - {item['topic'][:50]}... ({item['timestamp']})"):
                st.markdown(item['content'])
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.download_button(
                        label="📥 Download",
                        data=item['content'],
                        file_name=f"content_{i}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        key=f"download_{i}"
                    )
    else:
        st.info("📭 No content generated yet. Start creating content in the other tabs!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Marketing Command Center | Powered by Claude AI</p>
    <p><small>Configure your API key in the sidebar to start generating content</small></p>
</div>
""", unsafe_allow_html=True)
