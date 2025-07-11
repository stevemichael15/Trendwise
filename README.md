# 📈 TrendWise – Stock Market Analysis Web App

TrendWise is a user-friendly and visually interactive web app built with Flask that enables users to analyze, visualize, and understand stock market trends. It offers real-time and historical data visualizations, technical indicators, and an intuitive UI.

TrendWise Features:
- 🔐 User Authentication (Signup/Login)
- 📊 Stock Data Analysis: Volume, High, Low, Close
- 📈 Technical Indicators: SMA, EMA, etc.
- 🧠 Simple & Responsive Interface
- 🌐 Real-Time Data Fetching (via yFinance)
- 🖼️ Dynamic Chart Generation
- 🗃️ Organized and Modular Codebase

Tech Stack:
- Backend: Python (Flask)
- Frontend: HTML, CSS, Jinja2
- Charting: Matplotlib / Plotly
- Data Source: yFinance
- Environment: Virtualenv (venv)
- UI Framework: Bootstrap / Custom CSS

Folder Structure:
TrendWise/
├── main.py
├── extra_stuff.py
├── test_app.py
├── ideas.txt
├── requirements.txt
├── .gitignore
├── Templates/
│ ├── index.html
│ ├── intro.html
│ ├── home.html
│ ├── analysis.html
│ └── plot.html
├── static/
│ └── images/
│ ├── close_image.png
│ ├── high_image.png
│ ├── low_image.png
│ └── combined_image.png
├── media/
└── venv/

Installation Steps:
1.Clone the repo:
  git clone https://github.com/your-username/TrendWise.git
  cd TrendWise

2.Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate (On Windows: venv\Scripts\activate)

3.Install dependencies:
  pip install -r requirements.txt
  
4.Run the Flask app:
  python main.py

Visit http://localhost:5000 in your browser.


Planned Features:
- 📆 Time-range filters (1D, 1W, 1M, 1Y)
- 🔍 Auto-complete search bar for stocks
- 🧠 AI-based stock recommendations
- 💬 Integrated financial news feed
- ✅ Live price updates with WebSocket
- 💾 User watchlist and saved sessions

License:
MIT License

Copyright (c) 2025 Steve Prince

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

Author:
Steve Prince Michael  
GitHub: https://github.com/steveprince  
Email: stevemichael681@gmail.com

Contributing:
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Feedback:
If you find bugs or have feature requests, open an issue or email me directly.
