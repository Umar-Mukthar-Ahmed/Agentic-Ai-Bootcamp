"""
Prompt Library for Marketing Slogan Generator
==============================================
This module contains reusable prompt templates that follow best practices
in prompt engineering: clear role definition, explicit task specification,
and well-defined constraints.

Design Principles:
- Reusability: Templates work across different products and audiences
- Consistency: All prompts follow the Role-Task-Constraints pattern
- Maintainability: Each prompt is a separate function for easy updates
"""


def professional_slogan_prompt(product_name: str, target_audience: str, tone: str = "professional") -> str:
    """
    Generate a professional marketing slogan with strict quality controls.

    This prompt template enforces:
    - Role: Expert marketing copywriter with brand strategy experience
    - Task: Create 3 compelling, memorable slogans
    - Constraints: Word limit, tone specification, accuracy requirements

    Args:
        product_name: The product or service to market
        target_audience: The intended customer demographic
        tone: Desired communication style (default: professional)

    Returns:
        Formatted prompt string ready for API submission

    Reusability: Works for any product/audience combination by using
    variable injection rather than hardcoded values.
    """
    prompt = f"""You are an expert marketing copywriter with 10+ years of experience in brand strategy and consumer psychology.

Your task is to create 3 compelling marketing slogans for the following product:

Product: {product_name}
Target Audience: {target_audience}
Desired Tone: {tone}

Requirements and Constraints:
1. Each slogan must be between 3-8 words maximum
2. Slogans must be memorable, clear, and emotionally resonant
3. Maintain a {tone} tone throughout
4. Focus on customer benefits, not just product features
5. Do NOT make false claims or exaggerated promises
6. Avoid clichés like "best in class" or "world-leading"
7. Each slogan should be distinct and offer a different angle

Format your response as:
Slogan 1: [your slogan]
Slogan 2: [your slogan]
Slogan 3: [your slogan]

Brief Explanation: [One sentence explaining the strategic approach]"""

    return prompt


def creative_slogan_prompt(product_name: str, target_audience: str, tone: str = "bold") -> str:
    """
    Generate creative, attention-grabbing slogans with artistic freedom.

    This prompt template enforces:
    - Role: Creative director with expertise in disruptive marketing
    - Task: Develop innovative, memorable brand messages
    - Constraints: Creativity boundaries, word limits, ethical guidelines

    Args:
        product_name: The product or service to market
        target_audience: The intended customer demographic
        tone: Desired communication style (default: bold)

    Returns:
        Formatted prompt string ready for API submission

    Reusability: The creative framework applies to any industry while
    maintaining brand-appropriate boundaries through tone injection.
    """
    prompt = f"""You are a creative director at a leading advertising agency, known for creating viral campaigns and memorable brand identities.

Your task is to develop 3 innovative marketing slogans that break through the noise:

Product: {product_name}
Target Audience: {target_audience}
Desired Tone: {tone}

Creative Guidelines:
1. Maximum 7 words per slogan
2. Use vivid language, metaphors, or wordplay where appropriate
3. Maintain a {tone} and confident voice
4. Create an emotional connection or spark curiosity
5. Must be appropriate for professional marketing channels
6. Avoid misleading statements or unsubstantiated claims
7. Think outside conventional marketing language

Deliver 3 distinct slogans that each take a different creative approach:
- One focusing on aspiration
- One focusing on transformation
- One focusing on uniqueness

Format:
Slogan 1: [your slogan]
Slogan 2: [your slogan]
Slogan 3: [your slogan]

Creative Rationale: [One sentence on your creative strategy]"""

    return prompt


def audience_focused_prompt(product_name: str, target_audience: str, tone: str = "friendly") -> str:
    """
    Generate audience-centric slogans that speak directly to customer needs.

    This prompt template enforces:
    - Role: Consumer insights specialist with empathy-driven approach
    - Task: Create slogans that resonate with specific audience pain points
    - Constraints: Authenticity, relatability, length limits

    Args:
        product_name: The product or service to market
        target_audience: The intended customer demographic
        tone: Desired communication style (default: friendly)

    Returns:
        Formatted prompt string ready for API submission

    Reusability: The audience-first methodology adapts to any demographic
    by dynamically incorporating target audience characteristics.
    """
    prompt = f"""You are a consumer insights specialist who excels at understanding customer psychology and creating messages that deeply resonate with specific audiences.

Your task is to craft 3 audience-focused marketing slogans:

Product: {product_name}
Target Audience: {target_audience}
Desired Tone: {tone}

Audience-Centric Requirements:
1. Each slogan must be 4-8 words
2. Speak directly to the needs, desires, or challenges of {target_audience}
3. Use language and references this audience naturally uses
4. Maintain a {tone} and approachable tone
5. Build trust through authenticity, not hype
6. Ensure claims are realistic and verifiable
7. Make the audience feel understood and valued

Consider what matters most to {target_audience} and reflect that in your slogans.

Provide:
Slogan 1: [your slogan]
Slogan 2: [your slogan]
Slogan 3: [your slogan]

Audience Insight: [One sentence on why these resonate with {target_audience}]"""

    return prompt


def get_all_prompts(product_name: str, target_audience: str, tone: str = "professional") -> dict:
    """
    Convenience function to generate all prompt variations at once.

    Args:
        product_name: The product or service to market
        target_audience: The intended customer demographic
        tone: Desired communication style

    Returns:
        Dictionary with all three prompt templates populated

    Use Case: Allows comparison of different prompt strategies or
    batch generation for A/B testing campaigns.
    """
    return {
        "professional": professional_slogan_prompt(product_name, target_audience, tone),
        "creative": creative_slogan_prompt(product_name, target_audience, tone),
        "audience_focused": audience_focused_prompt(product_name, target_audience, tone)
    }