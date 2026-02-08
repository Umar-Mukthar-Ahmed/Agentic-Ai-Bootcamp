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
        githubUrl: "#",
    },
    {
        id: 2,
        week: 1,
        name: "Tech Article Summarizer",
        description: "Scrapes and summarizes technical blog posts and research papers. Extracts key takeaways tailored for developers.",
        tags: ["AI", "Web Scraping", "NLP"],
        stack: ["Python", "BeautifulSoup", "LangChain", "Streamlit"],
        status: "live",
        deployUrl: "https://example.com",
        githubUrl: "#",
    },
    {
        id: 3,
        week: 2,
        name: "Customer Support Agent",
        description: "AI-powered chatbot that handles customer queries, routes tickets, and escalates unresolved issues automatically.",
        tags: ["AI", "Chatbot", "Agents"],
        stack: ["Python", "FastAPI", "React", "LangChain"],
        status: "live",
        deployUrl: "https://example.com",
        githubUrl: "#",
    },
    {
        id: 4,
        week: 3,
        name: "Chat Interface Board",
        description: "A real-time chat board with AI-assisted message suggestions and topic threading built for team collaboration.",
        tags: ["Chatbot", "Real-time", "UI"],
        stack: ["React", "WebSockets", "Node.js", "MongoDB"],
        status: "in-progress",
        deployUrl: "#",
        githubUrl: "#",
    },
    {
        id: 5,
        week: 3,
        name: "AI Support Bot",
        description: "Autonomous support bot trained on internal docs. Answers FAQs, logs unresolved queries, and learns from feedback loops.",
        tags: ["AI", "Agents", "Automation"],
        stack: ["Python", "FastAPI", "Pinecone", "GPT-4"],
        status: "in-progress",
        deployUrl: "#",
        githubUrl: "#",
    },
    {
        id: 6,
        week: 3,
        name: "Sentiment Analysis API",
        description: "REST API that analyzes sentiment from text input using transformer models. Returns confidence scores and emotional tone.",
        tags: ["AI", "NLP", "API"],
        stack: ["Python", "FastAPI", "HuggingFace", "Docker"],
        status: "in-progress",
        deployUrl: "#",
        githubUrl: "#",
    },
    {
        id: 7,
        week: 4,
        name: "Document Q&A Engine",
        description: "Upload any document and ask questions about it. Powered by vector embeddings and retrieval-augmented generation.",
        tags: ["AI", "RAG", "NLP"],
        stack: ["Python", "LangChain", "Pinecone", "Streamlit"],
        status: "upcoming",
        deployUrl: "#",
        githubUrl: "#",
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

    // Add click handler to the button
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

    // Update results count
    resultsCount.textContent = `${filtered.length} project${filtered.length !== 1 ? "s" : ""} found`;

    // Clear container
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
    // Add mounted class for animations
    setTimeout(() => {
        document.getElementById("app").classList.add("mounted");
    }, 80);

    // Update stats
    updateStats();

    // Initial render
    renderProjects();

    // Search input handler
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", (e) => {
        currentQuery = e.target.value;
        renderProjects();
    });
}

/* ─── START APP ─── */
document.addEventListener("DOMContentLoaded", init);