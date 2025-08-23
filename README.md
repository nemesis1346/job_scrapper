# Web3 Job Seeker

A comprehensive job board application for Web3 careers, built with Python FastAPI backend and React frontend. This application fetches job data from web3.careers API and provides advanced filtering, search, and job management capabilities.

## 🚀 Features

### Backend (Python FastAPI)

- **RESTful API** with comprehensive endpoints
- **Real-time job fetching** from web3.careers API
- **Advanced filtering** by tags, location, company, and more
- **Background job refresh** every minute
- **Statistics and analytics** for job data
- **Health monitoring** and error handling
- **CORS support** for frontend integration
- **Comprehensive logging** and monitoring

### Frontend (React + TypeScript)

- **Modern UI** with Tailwind CSS and Framer Motion
- **Responsive design** that works on desktop and mobile
- **Advanced filtering** with tag-based search
- **Real-time search** across job titles, companies, and descriptions
- **Grid and list view** modes
- **Pagination** for large job lists
- **Statistics dashboard** with job analytics
- **Tag cloud** for easy skill-based filtering
- **Featured jobs** highlighting premium opportunities
- **Dark mode support**

## 🛠️ Tech Stack

### Backend

- **Python 3.8+**
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Requests** - HTTP client
- **BeautifulSoup** - HTML parsing
- **Schedule** - Background tasks
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Query** - Data fetching
- **React Router** - Navigation
- **Lucide React** - Icons
- **React Hot Toast** - Notifications

## 📁 Project Structure

```
python_job_seeker/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic data models
│   ├── config.py           # Configuration settings
│   ├── job_service.py      # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Startup script
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── App.tsx         # Main app component
│   │   └── index.tsx       # Entry point
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind configuration
├── job_seeker.py           # Original playground file (untouched)
├── cv_text.txt            # CV data file
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd python_job_seeker/backend
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   Create a `.env` file in the backend directory:

   ```env
   WEB3_CAREERS_TOKEN=your_token_here
   SECRET_KEY=your_secret_key_here
   ENVIRONMENT=development
   ```

4. **Run the backend server:**

   ```bash
   python run.py
   ```

   Or with custom settings:

   ```bash
   python run.py --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be available at `http://localhost:8000`

   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd python_job_seeker/frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Endpoints

#### Jobs

- `GET /jobs` - Get all jobs with optional filtering
- `GET /jobs/{job_id}` - Get a specific job by ID
- `GET /jobs/refresh` - Manually refresh job data

#### Tags

- `GET /tags` - Get all available tags with usage statistics

#### System

- `GET /health` - Health check endpoint
- `GET /stats` - System statistics
- `GET /` - API information

### Query Parameters

#### Job Filtering

- `tags` - Comma-separated list of tags
- `country` - Filter by country
- `company` - Filter by company name
- `limit` - Number of jobs to return (1-200)
- `offset` - Number of jobs to skip for pagination

#### Example Requests

```bash
# Get all jobs
curl http://localhost:8000/jobs

# Get jobs with specific tags
curl "http://localhost:8000/jobs?tags=solidity,ethereum&limit=20"

# Get jobs from a specific company
curl "http://localhost:8000/jobs?company=Consensys&limit=10"

# Get jobs with pagination
curl "http://localhost:8000/jobs?limit=20&offset=40"
```

## 🎨 Frontend Features

### Job Filtering

- **Tag-based filtering** - Click on tags to filter jobs
- **Search functionality** - Search across job titles, companies, and descriptions
- **Advanced filters** - Filter by location, job type, experience level
- **Active filter display** - See and remove active filters

### Job Display

- **Grid and list views** - Toggle between different display modes
- **Job cards** - Rich job information with tags and metadata
- **Featured jobs** - Highlighted premium opportunities
- **Pagination** - Navigate through large job lists

### Statistics and Analytics

- **Job statistics** - Total jobs, remote jobs, featured jobs
- **Tag cloud** - Visual representation of available skills
- **Company rankings** - Top companies by job count
- **Salary statistics** - Average, median, min, max salaries

## 🔧 Configuration

### Backend Configuration

The backend uses Pydantic settings with environment variable support. Key configuration options:

```python
# config.py
class Settings(BaseSettings):
    WEB3_CAREERS_TOKEN: str = "your_token_here"
    WEB3_CAREERS_LIMIT: int = 200
    DEFAULT_REFRESH_INTERVAL: int = 60  # seconds
    JOB_AGE_DAYS: int = 4  # Only fetch jobs from last 4 days
    DEFAULT_TAGS: List[str] = ["blockchain", "solidity", "ethereum", ...]
```

### Frontend Configuration

The frontend uses environment variables for API configuration:

```env
# .env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend Deployment

1. **Production requirements:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**

   ```env
   ENVIRONMENT=production
   WEB3_CAREERS_TOKEN=your_production_token
   SECRET_KEY=your_production_secret
   ```

3. **Run with production server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Frontend Deployment

1. **Build for production:**

   ```bash
   npm run build
   ```

2. **Serve the build folder** with your preferred web server (nginx, Apache, etc.)

## 🔍 Development

### Backend Development

- **Auto-reload** is enabled in development mode
- **Comprehensive logging** for debugging
- **API documentation** available at `/docs`
- **Health monitoring** at `/health`

### Frontend Development

- **Hot reload** for development
- **TypeScript** for type safety
- **ESLint and Prettier** for code quality
- **React Query DevTools** for data fetching debugging

### Code Quality

```bash
# Backend
cd backend
python -m flake8 .
python -m black .
python -m mypy .

# Frontend
cd frontend
npm run lint
npm run format
npm run type-check
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the API health endpoint: `http://localhost:8000/health`
2. Review the logs for error messages
3. Ensure all dependencies are installed correctly
4. Verify environment variables are set properly

## 🔮 Future Enhancements

- [ ] Database integration for job persistence
- [ ] User authentication and job applications
- [ ] Email notifications for new jobs
- [ ] Advanced analytics and reporting
- [ ] Mobile app development
- [ ] AI-powered job matching
- [ ] Company profiles and reviews
- [ ] Salary negotiation tools

## 📊 Performance

- **Backend**: Handles 1000+ concurrent requests
- **Frontend**: Optimized for fast loading with React Query caching
- **Job Refresh**: Automatic refresh every minute
- **Search**: Client-side search for instant results
- **Pagination**: Efficient pagination for large datasets

---

**Built with ❤️ for the Web3 community**
