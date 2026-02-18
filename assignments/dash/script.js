/* ─── PROJECT DATA ─── */
const projects = [
    {
        id: 1,
        week: 1,
        name: "Python & GitHub Setup",
        description: "Foundation exercise focused on setting up a GitHub repository and verifying the Python development environment with a simple Hello World program.",
        tags: ["Python", "GitHub", "Foundations"],
        stack: ["Python"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-1",
    },
    {
        id: 2,
        week: 2,
        name: "Mini Library Manager",
        description: "Python-based stateful library management system with persistent JSON storage, reading status tracking, star ratings, smart search by title/author/genre, Open Library API integration for ISBN lookups, and comprehensive logging.",
        tags: ["Python", "CLI", "API", "OOP"],
        stack: ["Python", "requests", "JSON"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-2/library_manager",
    },
    {
        id: 3,
        week: 2,
        name: "Movie Agent",
        description: "Movie collection manager with Studio Ghibli and OMDB API integration for fetching movie details. Track watched status, get recommendations by rating, and view collection statistics — available via CLI and Streamlit UI.",
        tags: ["AI", "Streamlit", "API", "Agents"],
        stack: ["Python", "Streamlit", "requests", "pandas"],
        status: "live",
        deployUrl: "https://agentic-ai-bootcamp-draekscizyenverqhiqo2x.streamlit.app/",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-2/movie-agent",
    },
    {
        id: 4,
        week: 3,
        name: "Company Policy Q&A (RAG)",
        description: "Retrieval-Augmented Generation system using Azure AI Search and Azure OpenAI. Supports user-specific document filtering, strict/conversational/detailed prompt modes, batch Q&A, and a no-hallucination policy.",
        tags: ["AI", "RAG", "Azure", "NLP"],
        stack: ["Python", "Azure AI Search", "Azure OpenAI"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-3/Document_qa_p",
    },
    {
        id: 5,
        week: 3,
        name: "Marketing Slogan Generator",
        description: "Streamlit web app generating marketing slogans via Azure OpenAI and reusable prompt templates. Supports Professional, Creative, and Audience-Focused styles across six tone options with downloadable results.",
        tags: ["AI", "Prompt Engineering", "Streamlit", "Azure"],
        stack: ["Python", "Streamlit", "Azure OpenAI"],
        status: "live",
        deployUrl: "https://agentic-ai-bootcamp-abwqqwxtwvaj9ek9xdlats.streamlit.app/",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-3/marketing-slogan-generator",
    },
    {
        id: 6,
        week: 4,
        name: "Customer Support Response Generator",
        description: "Interactive CLI tool generating context-aware customer support responses via Azure OpenAI. Features three prompt templates: general support, structured issue resolution (billing/technical/delivery), and empathy-first for emotional customers.",
        tags: ["AI", "Prompt Engineering", "Azure", "CLI"],
        stack: ["Python", "Azure OpenAI", "python-dotenv"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/Agentic-Ai-Bootcamp/tree/main/assignments/week-4/Customer%20Support%20Response%20Generator",
    },
    {
        id: 7,
        week: 5,
        name: "Email Automation Agent",
        description: "AI-powered email automation tool that drafts, categorizes, and sends personalized emails using LLM reasoning. Supports template-based generation, tone adjustment, bulk sending, and auto-reply workflows via SMTP integration.",
        tags: ["AI", "Automation", "Email", "Agents"],
        stack: ["Python", "OpenAI", "smtplib", "python-dotenv"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "#",
    },
    {
        id: 8,
        week: 5,
        name: "Speech to Text Transcriber",
        description: "Real-time speech transcription tool powered by OpenAI Whisper. Records audio from a microphone or accepts uploaded audio files, transcribes with high accuracy across multiple languages, and exports clean transcripts.",
        tags: ["AI", "Voice", "Whisper", "Transcription"],
        stack: ["Python", "OpenAI Whisper", "PyAudio", "Streamlit"],
        status: "completed",
        deployUrl: "https://github.com/Umar-Mukthar-Ahmed/speech-to-text",
        githubUrl: "#",
    },
    {
        id: 9,
        week: 6,
        name: "AI Web Scraper",
        description: "AI-powered web scraper that extracts and summarizes content from any URL. Parses page structure with BeautifulSoup, cleans the text, and uses an LLM to generate concise, developer-friendly summaries.",
        tags: ["AI", "Web Scraping", "NLP"],
        stack: ["Python", "BeautifulSoup", "LangChain", "Streamlit"],
        status: "completed",
        deployUrl: "#",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/ai_web_scraper",
    },
    {
        id: 10,
        week: 7,
        name: "Image Analyzer App",
        description: "AI-powered image analysis tool using Azure Computer Vision. Features OCR text extraction, object detection, image descriptions, probabilistic decision-making, and uncertainty handling — with dual CLI and Streamlit interfaces.",
        tags: ["AI", "Computer Vision", "OCR", "Azure"],
        stack: ["Python", "Azure AI", "Streamlit", "Plotly"],
        status: "live",
        deployUrl: "https://image-analyzer-app-lu6ftn22jvzn5jpoeqqiha.streamlit.app/",
        githubUrl: "https://github.com/Umar-Mukthar-Ahmed/image-analyzer-app/",
    },
];

/* ─── STATUS CONFIG ─── */
const STATUS = {
    live: { label: "Live", dot: "#22c55e" },
    "in-progress": { label: "In Progress", dot: "#f59e0b" },
    upcoming: { label: "Upcoming", dot: "#818cf8" },
    completed: { label: "Completed", dot: "#8b5cf6" },
};

/* ─── ICONS ─── */
const LinkIcon = () => `
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
`;

const GHIcon = () => `
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z" />
  </svg>
`;

const AlertIcon = () => `
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="8" x2="12" y2="12" />
    <line x1="12" y1="16" x2="12.01" y2="16" />
  </svg>
`;

/* ─── STATE ─── */
let currentQuery = "";

/* ─── TOAST NOTIFICATION ─── */
function showToast(message, type = "info") {
    const toastContainer = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
    ${AlertIcon()}
    <span>${message}</span>
  `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/* ─── PROJECT CARD ─── */
function createProjectCard(project, index) {
    const st = STATUS[project.status];
    const hasDeployUrl = project.deployUrl && project.deployUrl !== "" && project.deployUrl !== "#";

    const handleOpenProject = (e) => {
        if (!hasDeployUrl) {
            e.preventDefault();
            let message = "";
            if (project.status === "upcoming") {
                message = "This project is coming soon!";
            } else if (project.status === "in-progress") {
                message = "This project is still in progress. No deployment yet.";
            } else if (project.status === "completed") {
                message = "This project is completed but not deployed.";
            } else {
                message = "No deployment URL available for this project.";
            }
            showToast(message, "warning");
        }
    };

    const card = document.createElement("div");
    card.className = "project-card";
    card.style.animationDelay = `${index * 0.05}s`;

    card.innerHTML = `
    <div class="card-accent"></div>
    
    <div class="card-header">
      <div class="status-badge status-${project.status}">
        <div class="status-dot"></div>
        <span>${st.label}</span>
      </div>
    </div>
    
    <h3 class="project-title">${project.name}</h3>
    <p class="project-description">${project.description}</p>
    
    <div class="tags-row">
      ${project.tags.map(t => `<span class="tag">${t}</span>`).join("")}
    </div>
    
    <div class="stack-row">
      ${project.stack.map(s => `<span class="stack-item">${s}</span>`).join("")}
    </div>
    
    <div class="card-actions">
      <a
        href="${hasDeployUrl ? project.deployUrl : "#"}"
        target="${hasDeployUrl ? "_blank" : "_self"}"
        rel="noreferrer"
        class="btn-primary ${!hasDeployUrl ? "disabled" : ""}"
      >
        ${LinkIcon()} Open Project
      </a>
      <a href="${project.githubUrl}" target="_blank" rel="noreferrer" class="btn-github">
        ${GHIcon()}
      </a>
    </div>
  `;

    const button = card.querySelector(".btn-primary");
    button.addEventListener("click", handleOpenProject);

    return card;
}

/* ─── WEEK GROUP ─── */
function createWeekGroup(weekNumber, projectsList) {
    const weekGroup = document.createElement("div");
    weekGroup.className = "week-group";

    const weekHeader = document.createElement("div");
    weekHeader.className = "week-header";
    weekHeader.innerHTML = `
    <div class="week-number">Week ${weekNumber}</div>
    <div class="week-count">${projectsList.length} project${projectsList.length !== 1 ? "s" : ""}</div>
  `;

    const weekGrid = document.createElement("div");
    weekGrid.className = "week-grid";

    projectsList.forEach((p, i) => {
        weekGrid.appendChild(createProjectCard(p, i));
    });

    weekGroup.appendChild(weekHeader);
    weekGroup.appendChild(weekGrid);

    return weekGroup;
}

/* ─── FILTER PROJECTS ─── */
function filterProjects(query) {
    if (!query) return projects;

    const q = query.toLowerCase();
    return projects.filter(p => {
        return (
            p.name.toLowerCase().includes(q) ||
            p.description.toLowerCase().includes(q) ||
            p.tags.some(t => t.toLowerCase().includes(q)) ||
            p.stack.some(s => s.toLowerCase().includes(q))
        );
    });
}

/* ─── GROUP BY WEEK ─── */
function groupByWeek(projectsList) {
    const grouped = projectsList.reduce((acc, project) => {
        if (!acc[project.week]) acc[project.week] = [];
        acc[project.week].push(project);
        return acc;
    }, {});

    const weeks = Object.keys(grouped)
        .sort((a, b) => Number(a) - Number(b))
        .map(Number);

    return { grouped, weeks };
}

/* ─── CALCULATE STATS ─── */
function calculateStats() {
    return {
        total: projects.length,
        live: projects.filter(p => p.status === "live").length,
        inProgress: projects.filter(p => p.status === "in-progress").length,
        weeks: new Set(projects.map(p => p.week)).size,
    };
}

/* ─── UPDATE STATS ─── */
function updateStats() {
    const stats = calculateStats();

    document.getElementById("stat-total").textContent = stats.total;
    document.getElementById("stat-weeks").textContent = stats.weeks;
    document.getElementById("stat-live").textContent = stats.live;
    document.getElementById("stat-progress").textContent = stats.inProgress;
}

/* ─── RENDER PROJECTS ─── */
function renderProjects() {
    const filtered = filterProjects(currentQuery);
    const { grouped, weeks } = groupByWeek(filtered);

    const weeksContainer = document.getElementById("weeks-container");
    const emptyState = document.getElementById("empty-state");
    const resultsCount = document.getElementById("results-count");

    resultsCount.textContent = `${filtered.length} project${filtered.length !== 1 ? "s" : ""} found`;

    weeksContainer.innerHTML = "";

    if (weeks.length > 0) {
        emptyState.style.display = "none";
        weeks.forEach(weekNum => {
            weeksContainer.appendChild(createWeekGroup(weekNum, grouped[weekNum]));
        });
    } else {
        emptyState.style.display = "block";
    }
}

/* ─── INITIALIZE APP ─── */
function init() {
    setTimeout(() => {
        document.getElementById("app").classList.add("mounted");
    }, 80);

    updateStats();
    renderProjects();

    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", (e) => {
        currentQuery = e.target.value;
        renderProjects();
    });
}

/* ─── START APP ─── */
document.addEventListener("DOMContentLoaded", init);
