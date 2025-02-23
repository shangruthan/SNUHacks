def save_enhanced_resume_txt(enhanced_resume, output_path):
    """
    Save the enhanced resume as a .txt file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for heading, content in enhanced_resume.items():
            f.write(f"{heading}:\n")
            f.write(content + "\n\n")
    print(f"Enhanced resume saved to {output_path}")