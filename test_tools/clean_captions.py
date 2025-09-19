import re
import os


def clean_captions(input_file="captions_en.txt", output_file="cleaned_captions.txt"):
    """
    Clean caption text by removing timestamps and unnecessary characters
    
    Args:
        input_file (str): Path to the input caption file
        output_file (str): Path to save the cleaned captions
    
    Returns:
        str: Cleaned caption text
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return None
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"Original content length: {len(content)} characters")
        
        # Clean the content
        cleaned_text = clean_text(content)
        
        # Save cleaned text to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)
        
        print(f"Cleaned content length: {len(cleaned_text)} characters")
        print(f"Cleaned captions saved to: {output_file}")
        
        return cleaned_text
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None


def clean_text(text):
    """
    Clean the caption text by removing timestamps and formatting
    
    Args:
        text (str): Raw caption text with timestamps
    
    Returns:
        str: Cleaned text
    """
    
    # Step 1: Remove timestamp patterns like <01:13:29.320>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    
    # Step 2: Remove <c> and </c> tags
    text = re.sub(r'</?c>', '', text)
    
    # Step 3: Remove other HTML-like tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Step 4: Split into lines and process each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Remove duplicate consecutive lines (keep only unique consecutive lines)
        if not cleaned_lines or line != cleaned_lines[-1]:
            cleaned_lines.append(line)
    
    # Step 5: Join lines with proper spacing
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Step 6: Additional cleaning
    # Remove extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Fix spacing around punctuation
    cleaned_text = re.sub(r'\s+([,.!?;:])', r'\1', cleaned_text)
    
    # Ensure proper sentence spacing
    cleaned_text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', cleaned_text)
    
    # Split into sentences for better readability
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
    
    # Group sentences into paragraphs (every 3-5 sentences)
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if sentence:
            current_paragraph.append(sentence)
            
            # Create a new paragraph every 4 sentences or at natural breaks
            if len(current_paragraph) >= 4 or i == len(sentences) - 1:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
    
    # Join paragraphs with double newlines
    final_text = '\n\n'.join(paragraphs)
    
    return final_text


def preview_cleaning(input_file="captions_en.txt", lines_to_show=10):
    """
    Preview the cleaning process by showing before and after comparison
    
    Args:
        input_file (str): Path to the input caption file
        lines_to_show (int): Number of lines to show in preview
    """
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Show original content preview
        original_lines = content.split('\n')[:lines_to_show]
        print("=== ORIGINAL CONTENT (first 10 lines) ===")
        for line in original_lines:
            print(repr(line))
        
        print("\n" + "="*50)
        
        # Show cleaned content preview
        cleaned_content = clean_text(content)
        cleaned_lines = cleaned_content.split('\n')[:lines_to_show]
        print("=== CLEANED CONTENT (first 10 lines) ===")
        for line in cleaned_lines:
            print(repr(line))
        
    except Exception as e:
        print(f"Error previewing file: {str(e)}")


def main():
    """
    Main function to clean captions
    """
    input_file = "captions_en.txt"
    output_file = "cleaned_captions.txt"
    
    print("Caption Cleaner")
    print("=" * 30)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found!")
        print("Please make sure the captions file exists in the current directory.")
        return
    
    # Preview the cleaning process
    print("Preview of cleaning process:")
    preview_cleaning(input_file)
    
    print("\n" + "="*50)
    
    # Clean the captions
    cleaned_text = clean_captions(input_file, output_file)
    
    if cleaned_text:
        print(f"\n✅ Successfully cleaned captions!")
        print(f"📁 Input file: {input_file}")
        print(f"📄 Output file: {output_file}")
        
        # Show a sample of the cleaned text
        print("\n=== SAMPLE OF CLEANED TEXT ===")
        sample = cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
        print(sample)


if __name__ == "__main__":
    main()