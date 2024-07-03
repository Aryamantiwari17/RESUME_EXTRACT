import re
import json
import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_resume(resume_text):
    resume_dict = {}

    # Extract Personal Information
    name = re.search(r'Aryaman Tiwari', resume_text)
    email = re.search(r'Email:\s*([\w\.-]+@[\w\.-]+)', resume_text)
    phone = re.search(r'Mobile:\s*(\d+)', resume_text)
    github = re.search(r'Github/(\w+)', resume_text)
    linkedin = re.search(r'LinkedIn\s*/\s*(\w+)', resume_text)
    leetcode = re.search(r'LeetCode/(\w+)', resume_text)

    resume_dict["Personal Information"] = {
        "Name": name.group(0) if name else '',
        "Email": email.group(1) if email else '',
        "Mobile": phone.group(1) if phone else '',
        "GitHub": github.group(1) if github else '',
        "LinkedIn": linkedin.group(1) if linkedin else '',
        "LeetCode": leetcode.group(1) if leetcode else ''
    }

    # Extract Education
    education_match = re.search(r'EDUCATION[\s\S]*?(?=\n\n|\Z)', resume_text)
    if education_match:
        education_text = education_match.group(0).strip()
        institution = re.search(r'Jaypee University of Information Technology', education_text)
        degree = re.search(r'BTech in Computer Science', education_text)
        cgpa = re.search(r'CGPA:\s*([\d\.]+)', education_text)
        location = re.search(r'Solan, HP', education_text)
        duration = re.search(r'Sep\. 2021 – Jun\. 2025', education_text)

        resume_dict["Education"] = {
            "Institution": institution.group(0) if institution else '',
            "Degree": degree.group(0) if degree else '',
            "CGPA": float(cgpa.group(1)) if cgpa else '',
            "Location": location.group(0) if location else '',
            "Duration": duration.group(0) if duration else ''
        }

    # Extract Experience
    experience_list = []
    experience_match = re.search(r'EXPERIENCE[\s\S]*?(?=(PROJECTS|PROGRAMMING SKILLS|HONORS/ACHIEVEMENTS|\Z))', resume_text)
    if experience_match:
        experience_text = experience_match.group(0)
        exp_sections = experience_text.split('•')[1:]  # Split and remove the first empty split

        for section in exp_sections:
            company = re.search(r'^(.*?)(?:\n|$)', section).group(1).strip()
            position_match = re.search(r'Intern\s*\[([^\]]+)\]', section)
            position = 'Intern'
            technologies = position_match.group(1).split(', ') if position_match else []
            location_match = re.search(r'\((.*?)\)', section)
            location = location_match.group(1).strip() if location_match else ''
            duration_match = re.search(r'\b(\w+ \d+ - \w+ \d+)\b', section)
            duration = duration_match.group(1).strip() if duration_match else ''
            responsibilities = re.findall(r'◦ (.*?)\n', section)

            experience_list.append({
                "Company": company,
                "Position": position,
                "Technologies": technologies,
                "Location": location,
                "Duration": duration,
                "Responsibilities": [resp.strip() for resp in responsibilities]
            })

    resume_dict["Experience"] = experience_list

    # Extract Projects
    project_list = []
    project_match = re.search(r'PROJECTS[\s\S]*?(?=(PROGRAMMING SKILLS|HONORS/ACHIEVEMENTS|\Z))', resume_text)
    if project_match:
        project_text = project_match.group(0)
        project_sections = project_text.split('•')[1:]  # Split and remove the first empty split

        for section in project_sections:
            title_desc = re.search(r'^(.*?):\s*(.*?)(?:\n|$)', section)
            if title_desc:
                title, description = title_desc.groups()
                project_list.append({
                    "Title": title.strip(),
                    "Description": description.strip()
                })

    resume_dict["Projects"] = project_list

    # Extract Programming Skills
    skills_match = re.search(r'PROGRAMMING SKILLS[\s\S]*?(?=HONORS/ACHIEVEMENTS)', resume_text)
    if skills_match:
        skills_text = skills_match.group(0).strip()
        languages = re.search(r'Languages\s*:\s*(.*?)\n', skills_text)
        technologies = re.search(r'Technologies/Frameworks\s*:\s*(.*?)\n', skills_text)
        others = re.search(r'Others\s*:\s*(.*?)\n', skills_text)

        resume_dict["Programming Skills"] = {
            "Languages": languages.group(1).strip().split(', ') if languages else [],
            "Technologies/Frameworks": technologies.group(1).strip().split(', ') if technologies else [],
            "Others": others.group(1).strip().split(', ') if others else []
        }

    # Extract Honors/Achievements
    honors_list = []
    honors_match = re.search(r'HONORS/ACHIEVEMENTS[\s\S]*', resume_text)
    if honors_match:
        honors_text = honors_match.group(0)
        honor_sections = honors_text.split('•')[1:]  # Split and remove the first empty split

        for section in honor_sections:
            title_desc = re.search(r'^(.*?):\s*(.*?)(?:\n|$)', section)
            if title_desc:
                title, description = title_desc.groups()
                honors_list.append({
                    "Title": title.strip(),
                    "Description": description.strip()
                })

    resume_dict["Honors/Achievements"] = honors_list

    return resume_dict

# Example usage:
file_path = '/home/aryaman/CV/updated_aryaman.pdf'
resume_text = extract_text_from_pdf(file_path)
#print("Extracted Resume Text:\n", resume_text)  # Debugging step
resume_data = parse_resume(resume_text)

# Convert the parsed resume data to JSON format
resume_json = json.dumps(resume_data, indent=4)
print(resume_json)
