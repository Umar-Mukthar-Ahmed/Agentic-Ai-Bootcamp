import { useState, useEffect } from "react";
import "./App.css";

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

/* ─── ICONS ─── */
const SearchIcon = () => (
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
);

const LinkIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);

const GHIcon = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z" />
  </svg>
);

const AlertIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="8" x2="12" y2="12" />
    <line x1="12" y1="16" x2="12.01" y2="16" />
  </svg>
);

/* ─── STATUS CONFIG ─── */
const STATUS = {
  live: { label: "Live", dot: "#22c55e" },
  "in-progress": { label: "In Progress", dot: "#f59e0b" },
  upcoming: { label: "Upcoming", dot: "#818cf8" },
  completed: { label: "Completed", dot: "#8b5cf6" },
};

/* ─── TOAST NOTIFICATION ─── */
function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast toast-${type}`}>
      <AlertIcon />
      <span>{message}</span>
    </div>
  );
}

/* ─── PROJECT CARD ─── */
function ProjectCard({ project, index, onShowToast }) {
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
      onShowToast(message, "warning");
    }
  };

  return (
    <div className="project-card" style={{ animationDelay: `${index * 0.05}s` }}>
      <div className="card-accent" />

      <div className="card-header">
        <div className={`status-badge status-${project.status}`}>
          <div className="status-dot" />
          <span>{st.label}</span>
        </div>
      </div>

      <h3 className="project-title">{project.name}</h3>
      <p className="project-description">{project.description}</p>

      <div className="tags-row">
        {project.tags.map((t) => (
          <span key={t} className="tag">
            {t}
          </span>
        ))}
      </div>

      <div className="stack-row">
        {project.stack.map((s) => (
          <span key={s} className="stack-item">
            {s}
          </span>
        ))}
      </div>

      <div className="card-actions">
        <a
          href={hasDeployUrl ? project.deployUrl : "#"}
          target={hasDeployUrl ? "_blank" : "_self"}
          rel="noreferrer"
          className={`btn-primary ${!hasDeployUrl ? "disabled" : ""}`}
          onClick={handleOpenProject}
        >
          <LinkIcon /> Open Project
        </a>
        <a href={project.githubUrl} target="_blank" rel="noreferrer" className="btn-github">
          <GHIcon />
        </a>
      </div>
    </div>
  );
}

/* ─── WEEK GROUP ─── */
function WeekGroup({ weekNumber, projects, onShowToast }) {
  return (
    <div className="week-group">
      <div className="week-header">
        <div className="week-number">Week {weekNumber}</div>
        <div className="week-count">{projects.length} project{projects.length !== 1 ? "s" : ""}</div>
      </div>
      <div className="week-grid">
        {projects.map((p, i) => (
          <ProjectCard key={p.id} project={p} index={i} onShowToast={onShowToast} />
        ))}
      </div>
    </div>
  );
}

/* ─── MAIN APP ─── */
export default function App() {
  const [query, setQuery] = useState("");
  const [mounted, setMounted] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setMounted(true), 80);
    return () => clearTimeout(timer);
  }, []);

  const showToast = (message, type = "info") => {
    setToast({ message, type });
  };

  const closeToast = () => {
    setToast(null);
  };

  // Filter projects
  const filtered = projects.filter((p) => {
    if (!query) return true;
    const q = query.toLowerCase();
    return (
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some((t) => t.toLowerCase().includes(q)) ||
      p.stack.some((s) => s.toLowerCase().includes(q))
    );
  });

  // Group by week
  const groupedByWeek = filtered.reduce((acc, project) => {
    if (!acc[project.week]) acc[project.week] = [];
    acc[project.week].push(project);
    return acc;
  }, {});

  const weeks = Object.keys(groupedByWeek)
    .sort((a, b) => Number(a) - Number(b))
    .map(Number);

  // Stats
  const stats = {
    total: projects.length,
    live: projects.filter((p) => p.status === "live").length,
    inProgress: projects.filter((p) => p.status === "in-progress").length,
    weeks: new Set(projects.map((p) => p.week)).size,
  };

  return (
    <div className={`app ${mounted ? "mounted" : ""}`}>
      <div className="ambient-glow glow-top" />
      <div className="ambient-glow glow-bottom" />

      {/* Toast Notification */}
      {toast && <Toast message={toast.message} type={toast.type} onClose={closeToast} />}

      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-badge">
            <div className="pulse-dot" />
            <code>Agentic-AI-Bootcamp / dashboard</code>
          </div>
          <h1 className="title">Project Hub</h1>
          <p className="subtitle">All weekly assignments — organized, deployed, tracked.</p>
        </header>

        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Projects</div>
            <div className="stat-value" style={{ color: "#06b6d4" }}>
              {stats.total}
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Weeks</div>
            <div className="stat-value" style={{ color: "#818cf8" }}>
              {stats.weeks}
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Live</div>
            <div className="stat-value" style={{ color: "#22c55e" }}>
              {stats.live}
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-label">In Progress</div>
            <div className="stat-value" style={{ color: "#f59e0b" }}>
              {stats.inProgress}
            </div>
          </div>
        </div>

        {/* Search */}
        <div className="search-section">
          <div className="search-box">
            <SearchIcon />
            <input
              type="text"
              placeholder="Search projects, tags, or tech stack…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        {/* Results count */}
        <div className="results-count">
          {filtered.length} project{filtered.length !== 1 ? "s" : ""} found
        </div>

        {/* Week Groups */}
        {weeks.length > 0 ? (
          <div className="weeks-container">
            {weeks.map((weekNum) => (
              <WeekGroup
                key={weekNum}
                weekNumber={weekNum}
                projects={groupedByWeek[weekNum]}
                onShowToast={showToast}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">No projects match your search.</div>
        )}

        {/* Footer */}
        <footer className="footer">
          <span>Agentic-AI-Bootcamp · central dashboard</span>
          <span>Replace empty URLs with deployed links</span>
        </footer>
      </div>
    </div>
  );
}