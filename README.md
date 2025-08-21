# Resume-Filter

Resume-Filter is a Django-based web application that streamlines the recruitment process by intelligently matching uploaded resumes against job descriptions. It leverages Natural Language Processing (NLP) techniques to classify candidates based on their fit for the job, helping recruiters efficiently shortlist suitable candidates.

## Features

- **Resume Parsing:** Upload multiple resumes (PDF, DOCX) and automatically extract candidate information.
- **Job Description Analysis:** Input or upload job descriptions to set the requirements for candidate matching.
- **Intelligent Matching:** Uses NLP and machine learning to compare resumes with job descriptions and score candidate relevance.
- **Candidate Classification:** Automatically classifies and ranks candidates based on match scores.
- **User-Friendly Dashboard:** View results, matched candidates, and manage ongoing recruitment processes.
- **Secure Authentication:** User registration and login for recruiters.

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **NLP:** spaCy, scikit-learn
- **Database:** SQLite (default, easily switchable to PostgreSQL or MySQL)
- **File Handling:** python-docx, PyPDF2

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sandiya1/Resume-Filter.git
   cd Resume-Filter
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

### Usage

1. Get started in the home page.
2. Upload job descriptions.
3. Upload resumes (PDF or DOCX).
4. View matched candidates and their fit scores.
5. Send automated mails to selecte and rejected candidates.

## Project Structure

```
Resume-Filter/
├── resume_filter/      # Django project settings
├── matcher/            # Main app: models, views, templates
├── media/              # Uploaded resumes
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome!
- Fork the repository
- Create your feature branch (`git checkout -b feature/new-feature`)
- Commit your changes (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature/new-feature`)
- Open a pull request



## Contact

For questions or suggestions, feel free to open an issue or contact [Sandiya1](https://github.com/Sandiya1) , sandiya1804@gmail.com.

## Note

In settings, use your gmail Id and create the app password in google. "don't use your gmail password"
