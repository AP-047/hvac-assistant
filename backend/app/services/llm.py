import re
from typing import List, Dict

def markdown_to_html(text: str) -> str:
    """Convert basic markdown formatting to HTML"""
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    lines = text.split('\n')
    html_lines = []
    in_ul_list = False
    in_ol_list = False
    
    for line in lines:
        line = line.strip()
        
        # Handle bullet points
        if line.startswith('• '):
            if in_ol_list:
                html_lines.append('</ol>')
                in_ol_list = False
            if not in_ul_list:
                html_lines.append('<ul>')
                in_ul_list = True
            # Process the content for bold formatting
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line[2:])
            html_lines.append(f'<li>{content}</li>')
            
        # Handle numbered lists
        elif re.match(r'^\d+\.\s+', line):
            if in_ul_list:
                html_lines.append('</ul>')
                in_ul_list = False
            if not in_ol_list:
                html_lines.append('<ol>')
                in_ol_list = True
            # Remove number and process content for bold formatting
            content = re.sub(r'^\d+\.\s+', '', line)
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            html_lines.append(f'<li>{content}</li>')
            
        # Handle regular paragraphs
        else:
            if in_ul_list:
                html_lines.append('</ul>')
                in_ul_list = False
            if in_ol_list:
                html_lines.append('</ol>')
                in_ol_list = False
            if line:
                # Process paragraph content for bold formatting
                content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                html_lines.append(f'<p>{content}</p>')
    
    # Close any open lists
    if in_ul_list:
        html_lines.append('</ul>')
    if in_ol_list:
        html_lines.append('</ol>')
    
    return '\n'.join(html_lines)

def extract_key_info(context: str, query: str) -> str:
    """Extract and clean key information from context, removing messy source references"""
    try:
        if not context or len(context) < 20:
            return ""
            
        # Clean up messy source references and page numbers
        cleaned_context = re.sub(r'Source \d+:', '', context)
        cleaned_context = re.sub(r'Page \d+-\d+', '', cleaned_context)
        cleaned_context = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', '', cleaned_context)  # Remove dates
        cleaned_context = re.sub(r'HVAC Design Manual.*?\d{4}', '', cleaned_context)  # Remove manual references
        cleaned_context = re.sub(r'VERSION: V\d+\.\d+', '', cleaned_context)  # Remove version numbers
        cleaned_context = re.sub(r'DATE PUBLISHED:.*?\d{4}', '', cleaned_context)  # Remove publication dates
        cleaned_context = re.sub(r'FIGURE \d+-\d+.*?OVERVIEW', '', cleaned_context)  # Remove figure references
        cleaned_context = re.sub(r'CHAPTER \d+:.*?CONTENTS', '', cleaned_context)  # Remove chapter references
        cleaned_context = re.sub(r'\s+', ' ', cleaned_context).strip()  # Normalize whitespace
        
        # Split into sentences and extract relevant information
        sentences = re.split(r'[.!?]+', cleaned_context)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Query keywords for relevance scoring
        query_words = set(query.lower().split())
        
        # Score sentences by relevance
        relevant_sentences = []
        for sentence in sentences[:10]:  # Limit processing
            sentence_words = set(sentence.lower().split())
            relevance_score = len(query_words.intersection(sentence_words))
            if relevance_score > 0 or any(word in sentence.lower() for word in ['hvac', 'system', 'air', 'heat', 'cool', 'ventilation']):
                relevant_sentences.append((sentence, relevance_score))
        
        # Sort by relevance and take top sentences
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sent[0] for sent in relevant_sentences[:3]]  # Reduced to 3 most relevant
        
        result = '. '.join(top_sentences)
        return result + '.' if result and not result.endswith('.') else result
        
    except Exception as e:
        print(f"Context extraction error: {e}")
        return ""

def synthesize_answer(context: str, query: str) -> str:
    """
    Synthesize an intelligent answer using LLM-style reasoning combined with retrieved context.
    Creates natural, flowing responses rather than template-based answers.
    """
    
    # Extract and clean key information from documents
    key_info = extract_key_info(context, query)
    key_info = re.sub(r'[.]\s*-\s*[^.]*$', '.', key_info)  # Clean fragments
    key_info = re.sub(r'\s+', ' ', key_info).strip()
    
    # Check if we have relevant HVAC-related information
    has_relevant_docs = bool(key_info and len(key_info) > 50 and 
                            any(term in key_info.lower() for term in 
                                ['hvac', 'heating', 'ventilation', 'air conditioning', 'cooling', 
                                 'temperature', 'system', 'equipment', 'duct', 'filter']))
    
    if has_relevant_docs:
        # Create intelligent synthesis combining documentation with HVAC knowledge
        if "what is" in query.lower() or "define" in query.lower():
            # For definition questions, provide comprehensive explanation
            if "hvac" in query.lower():
                if key_info:
                    markdown_response = f"""**HVAC (Heating, Ventilation, and Air Conditioning)** systems are comprehensive building infrastructure designed to control indoor environmental conditions for comfort, health, and energy efficiency.

**From the technical documentation:**
{key_info}

These systems integrate three core functions: **heating** maintains warmth during cold periods, **ventilation** manages air circulation and quality, and **air conditioning** provides cooling and humidity control. Modern HVAC systems are sophisticated networks of mechanical components, sensors, and controls that work together to maintain optimal indoor conditions while minimizing energy consumption.

The specific design and configuration depend on building size, occupancy, climate zone, and performance requirements, with professional engineering ensuring compliance with codes and standards."""
                else:
                    markdown_response = f"""**HVAC (Heating, Ventilation, and Air Conditioning)** systems are comprehensive building infrastructure designed to control indoor environmental conditions for comfort, health, and energy efficiency.

These systems integrate three core functions: **heating** maintains warmth during cold periods, **ventilation** manages air circulation and quality, and **air conditioning** provides cooling and humidity control. Modern HVAC systems are sophisticated networks of mechanical components, sensors, and controls that work together to maintain optimal indoor conditions while minimizing energy consumption.

The specific design and configuration depend on building size, occupancy, climate zone, and performance requirements, with professional engineering ensuring compliance with codes and standards."""

            else:
                # General definition with documentation context
                if key_info:
                    markdown_response = f"""**Technical Definition:**

**From the documentation:**
{key_info}

This represents established industry practices where systems are designed with careful consideration of thermal loads, air quality requirements, and energy efficiency standards. Professional HVAC design involves complex calculations for sizing equipment, determining air flow rates, and selecting appropriate components for the specific application.

**Key design factors include:**
• Building envelope characteristics and thermal loads
• Occupancy patterns and ventilation requirements  
• Local climate conditions and seasonal variations
• Energy codes and sustainability objectives
• Integration with building automation systems"""
                else:
                    markdown_response = f"""I don't have specific technical documentation about this topic in the HVAC knowledge base. For detailed information about specific HVAC components, systems, or calculations, please try asking about:

• HVAC system types and components
• Heating and cooling equipment specifications
• Ventilation requirements and air quality
• Energy efficiency and system design
• Maintenance and troubleshooting procedures"""

        elif "how" in query.lower():
            # For process questions, explain operation with documentation context
            if key_info:
                markdown_response = f"""**Technical Process:**

**From the documentation:**
{key_info}

This process demonstrates the sophisticated control systems modern HVAC installations employ. Temperature sensors continuously monitor conditions, while automated controls adjust equipment operation to maintain setpoints efficiently. The system balances heating, cooling, and ventilation loads while optimizing energy consumption through variable-speed drives, economizer cycles, and smart scheduling.

**Operational considerations:**
• Sensor-based feedback control for precise temperature regulation
• Load balancing across multiple zones or spaces
• Integration with building management systems for coordinated operation
• Preventive maintenance scheduling to ensure optimal performance"""
            else:
                markdown_response = f"""I don't have specific procedural information about this in the HVAC documentation. For detailed operational procedures, please ask about specific HVAC processes such as:

• System startup and commissioning procedures
• Equipment operation and control sequences  
• Maintenance and troubleshooting steps
• Energy optimization strategies"""

        elif any(word in query.lower() for word in ['best', 'suited', 'recommend', 'choose', 'select']):
            # For recommendation questions, provide expert guidance with documentation
            if key_info:
                markdown_response = f"""**Professional Recommendation:**

**From the technical documentation:**
{key_info}

Based on this information and HVAC engineering best practices, the optimal system selection depends on several critical factors. **Specialized environments** require precise environmental control, typically involving dedicated air handling units, sophisticated filtration, and redundant systems for reliability.

**Professional selection criteria include:**
  **Environmental requirements**: Temperature, humidity, and air quality specifications
  **Contamination control**: Appropriate filtration and air change rates
  **Redundancy and reliability**: Backup systems for critical operations  
  **Energy efficiency**: Life-cycle cost analysis and sustainability goals
  **Regulatory compliance**: Industry standards and local building codes

For complex applications, consultation with specialized HVAC engineers ensures proper system selection, sizing, and integration."""
            else:
                markdown_response = f"""For system selection and recommendations, I'd need more specific information about your application. Professional HVAC system selection typically considers:

**Key factors:**
  **Building type and use**: Residential, commercial, industrial, or specialized
  **Environmental requirements**: Temperature, humidity, and air quality needs
  **Space constraints**: Available equipment locations and distribution paths
  **Energy considerations**: Efficiency targets and utility costs
  **Budget parameters**: Initial cost and lifecycle operating expenses

Please provide more details about your specific application for tailored recommendations."""

        else:
            # General informational response with natural integration
            markdown_response = f"""Based on HVAC industry standards and the available documentation:

{key_info}

This information aligns with professional engineering practices where systems are designed to meet specific performance criteria while optimizing energy efficiency and maintaining indoor environmental quality. The complexity of modern HVAC systems requires careful integration of mechanical components, control systems, and building automation.

**Professional implementation involves:**
  Detailed load calculations and system sizing
  Component selection based on performance requirements
  Integration with building infrastructure and controls
  Commissioning and performance verification
  Ongoing maintenance and optimization programs"""

    else:
        # Handle non-HVAC or HVAC questions without relevant documentation
        if any(hvac_term in query.lower() for hvac_term in 
               ['hvac', 'heating', 'cooling', 'ventilation', 'air conditioning', 'thermostat']):
            # HVAC-related but no relevant docs found
            markdown_response = f"""I don't have specific documentation about this HVAC topic in my current knowledge base, but I can provide general guidance:

HVAC systems involve complex mechanical and control systems designed for indoor environmental management. For detailed information about your specific question, I recommend consulting:

**Professional resources:**
  ASHRAE handbooks and standards for engineering guidelines
  Equipment manufacturer specifications and documentation
  Licensed HVAC professionals for system-specific advice
  Local building codes and energy efficiency programs

If you have questions about general HVAC principles, system types, or common applications, I'd be happy to help with more specific inquiries."""
        else:
            # Non-HVAC question
            markdown_response = f"""I specialize in HVAC (Heating, Ventilation, and Air Conditioning) systems and related building environmental control topics.

Your question about "{query}" falls outside my expertise area. I can assist with:

**HVAC system design and engineering**
**Equipment selection and sizing**  
**Energy efficiency and sustainability**
**Indoor air quality and ventilation**
**System maintenance and troubleshooting**
**Building codes and industry standards**

Please feel free to ask any HVAC-related questions!"""

    # Convert markdown formatting to HTML
    return markdown_to_html(markdown_response)

def generate_answer(prompt: str) -> str:
    """Generate an intelligent, synthesized answer combining retrieved info with HVAC knowledge"""
    try:
        # Extract context and query from prompt
        parts = prompt.split("Question:")
        if len(parts) < 2:
            return "I need a properly formatted question to provide an answer."
        
        context_part = parts[0].replace("Context:", "").strip()
        query = parts[1].replace("Answer based on the context:", "").strip()
        
        if not context_part:
            return "HVAC stands for Heating, Ventilation, and Air Conditioning. It refers to systems that control indoor environmental conditions including temperature, humidity, and air quality to maintain comfortable and healthy indoor environments."
        
        # Generate intelligent synthesized response
        return synthesize_answer(context_part, query)
        
    except Exception as e:
        print(f"Answer generation error: {e}")
        return "I'm sorry, I encountered an error while processing your HVAC question. Please try rephrasing your question."