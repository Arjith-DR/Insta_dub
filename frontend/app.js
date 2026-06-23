const API_BASE = "/api";
const TOKEN_KEY = "insta_token";
const USER_KEY = "insta_user";
const ADMIN_KEY = "insta_is_admin";

const icons = {
  home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m3 10.5 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
  search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
  compass: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.1 5-5 2.1 2.1-5 5-2.1Z"/></svg>',
  film: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 4h16v16H4z"/><path d="m9 8 6 4-6 4V8Z"/><path d="M8 4v16M16 4v16"/></svg>',
  heart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 1 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8Z"/></svg>',
  image: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.5" cy="10.5" r="1.5"/><path d="m21 15-5-5L5 19"/></svg>',
  "plus-square": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 8v8M8 12h8"/></svg>',
  "log-out": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/></svg>',
  shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/></svg>',
  more: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></svg>',
  bookmark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M6 3h12v18l-6-4-6 4V3Z"/></svg>',
  message: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 12a8.5 8.5 0 0 1-8.5 8.5 9.5 9.5 0 0 1-4.3-1L3 21l1.5-4.4A8.5 8.5 0 1 1 21 12Z"/></svg>',
  trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 14h10l1-14M9 7V4h6v3"/></svg>',
  x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M18 6 6 18M6 6l12 12"/></svg>'
};

const demoUsers = [
  { user_id: "demo-1", email: "maya.studio@example.com", status: "active" },
  { user_id: "demo-2", email: "alex.city@example.com", status: "active" },
  { user_id: "demo-3", email: "nina.frames@example.com", status: "active" }
];

const demoPosts = [
  { post_id: "demo-post-1", user_id: "demo-1", caption: "Soft light, clean lines, and a tiny corner that finally feels finished.", image_url: "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1200&q=80", location: "Design District", likes: 12842, comments: 312 },
  { post_id: "demo-post-2", user_id: "demo-2", caption: "Evening walk, bright windows, no hurry.", image_url: "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80", location: "Downtown", likes: 9821, comments: 145 },
  { post_id: "demo-post-3", user_id: "demo-3", caption: "Posting this before the coffee gets cold.", image_url: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80", location: "Cafe Linea", likes: 6420, comments: 98 }
];

const demoReels = [
  { reel_id: "demo-reel-1", user_id: "demo-1", caption: "Three seconds before the sunset changed everything.", video_url: "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", image_url: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80", location: "Golden hour", likes: 22014, comments: 684 }
];

const state = {
  token: localStorage.getItem(TOKEN_KEY) || "",
  isAdmin: localStorage.getItem(ADMIN_KEY) === "true",
  users: [],
  posts: [],
  reels: [],
  currentUserId: localStorage.getItem(USER_KEY) || null,
  view: "posts",
  activeNav: "home",
  usingDemo: false,
  liked: new Set(),
  saved: new Set(),
  openComments: new Set(),
  commentStore: new Map(),
  selectedPhotoDataUrl: "",
  selectedVideoDataUrl: "",
  adminUsers: [],
  roles: []
};

const els = {
  loginScreen: document.getElementById("loginScreen"),
  appShell: document.getElementById("appShell"),
  loginForm: document.getElementById("loginForm"),
  quickSignupForm: document.getElementById("quickSignupForm"),
  loginError: document.getElementById("loginError"),
  feedView: document.getElementById("feedView"),
  profileView: document.getElementById("profileView"),
  adminView: document.getElementById("adminView"),
  feed: document.getElementById("feed"),
  storiesStrip: document.getElementById("storiesStrip"),
  adminNavItem: document.getElementById("adminNavItem"),
  createDialog: document.getElementById("createDialog"),
  createPostForm: document.getElementById("createPostForm"),
  createReelForm: document.getElementById("createReelForm"),
  savedView: document.getElementById("savedView"),
  newPostPhoto: document.getElementById("newPostPhoto"),
  newReelVideo: document.getElementById("newReelVideo"),
  postPhotoPreview: document.getElementById("postPhotoPreview"),
  reelVideoPreview: document.getElementById("reelVideoPreview")
};

function icon(name) {
  return icons[name] || "";
}

function hydrateIcons(root = document) {
  root.querySelectorAll("[data-icon]").forEach((node) => {
    node.innerHTML = icon(node.dataset.icon);
  });
}

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    let message = `Request failed: ${response.status}`;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {}
    throw new Error(message);
  }
  return response.status === 204 ? null : response.json();
}

function usernameFrom(user) {
  const raw = (user?.username || user?.email || `user${user?.user_id || ""}`).split("@")[0];
  return raw.replace(/[^a-zA-Z0-9._]/g, ".").replace(/\.+/g, ".").replace(/^\./, "") || "instagram_user";
}

function initialsFrom(name) {
  return name.split(/[._\s-]+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase() || "IG";
}

function escapeHtml(value) {
  const span = document.createElement("span");
  span.textContent = value == null ? "" : String(value);
  return span.innerHTML;
}

function currentUser() {
  return state.users.find((user) => String(user.user_id) === String(state.currentUserId)) || state.users[0] || demoUsers[0];
}

function userById(id) {
  return state.users.find((user) => String(user.user_id) === String(id));
}

function setAuthenticated(token, isAdmin, userId) {
  state.token = token;
  state.isAdmin = isAdmin;
  if (userId) state.currentUserId = String(userId);
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(ADMIN_KEY, String(isAdmin));
  if (state.currentUserId) localStorage.setItem(USER_KEY, state.currentUserId);
}

function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(ADMIN_KEY);
  state.token = "";
  state.currentUserId = null;
  state.isAdmin = false;
  els.appShell.classList.add("is-hidden");
  els.loginScreen.classList.remove("is-hidden");
}

async function login(event) {
  event.preventDefault();
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;
  const wantsAdmin = document.getElementById("adminLogin").checked;
  const button = document.getElementById("loginButton");

  els.loginError.textContent = "";
  button.disabled = true;
  button.textContent = "Logging in...";
  try {
    const result = await api("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    state.token = result.access_token;
    const users = await api("/users/");
    const user = users.find((item) => item.email === email) || users[0];
    setAuthenticated(result.access_token, false, user?.user_id);
    if (wantsAdmin) {
      await api("/admin/users/");
      setAuthenticated(result.access_token, true, user?.user_id);
    }
    await bootApp();
  } catch (error) {
    state.token = "";
    els.loginError.textContent = wantsAdmin ? `Admin login failed: ${error.message}` : error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Log in";
  }
}

async function quickSignup(event) {
  event.preventDefault();
  const email = document.getElementById("signupEmail").value.trim();
  const password = document.getElementById("signupPassword").value;
  try {
    await api("/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role_id: 1, email, password, status: "active" })
    });
    document.getElementById("loginEmail").value = email;
    document.getElementById("loginPassword").value = password;
    els.quickSignupForm.reset();
    els.loginError.textContent = "Account created. Log in now.";
  } catch (error) {
    els.loginError.textContent = error.message;
  }
}

async function loadUsers() {
  try {
    const users = await api("/users/");
    state.users = users.length ? users : [...demoUsers];
    state.usingDemo = !users.length;
  } catch {
    state.users = [...demoUsers];
    state.usingDemo = true;
  }
  if (!state.currentUserId && state.users.length) state.currentUserId = state.users[0].user_id;
}

async function loadFeed() {
  try {
    const requesterId = Number(state.currentUserId) || 1;
    const [posts, reels] = await Promise.all([
      api(`/posts/?requester_id=${encodeURIComponent(requesterId)}`),
      api(`/reels/?requester_id=${encodeURIComponent(requesterId)}`)
    ]);
    state.posts = enrichPosts(posts.length ? posts : demoPosts);
    state.reels = enrichReels(reels.length ? reels : demoReels);
    state.usingDemo = state.usingDemo || (!posts.length && !reels.length);
  } catch {
    state.posts = enrichPosts(demoPosts);
    state.reels = enrichReels(demoReels);
    state.usingDemo = true;
  }
}

function enrichPosts(posts) {
  const images = demoPosts.map((post) => post.image_url);
  return posts.map((post, index) => ({
    ...post,
    image_url: post.image_url || images[index % images.length],
    likes: post.likes ?? (String(post.post_id).startsWith("demo-") ? 120 + index * 43 : 0),
    comments: post.comments ?? (String(post.post_id).startsWith("demo-") ? 5 + index * 2 : 0),
    location: post.location || "Instagram"
  }));
}

function enrichReels(reels) {
  return reels.map((reel, index) => ({
    ...reel,
    image_url: reel.image_url || demoReels[index % demoReels.length].image_url,
    video_url: reel.video_url || demoReels[0].video_url,
    likes: reel.likes ?? (String(reel.reel_id).startsWith("demo-") ? 330 + index * 91 : 0),
    comments: reel.comments ?? (String(reel.reel_id).startsWith("demo-") ? 12 + index * 3 : 0),
    location: reel.location || "Reels"
  }));
}

function renderStories() {
  els.storiesStrip.innerHTML = state.users.map((user) => {
    const username = usernameFrom(user);
    return `
      <button class="story-button" type="button">
        <span class="story-ring"><span class="story-avatar">${escapeHtml(initialsFrom(username))}</span></span>
        <span>${escapeHtml(username)}</span>
      </button>
    `;
  }).join("");
}

function renderFeed() {
  const items = state.view === "reels" ? state.reels : state.posts;
  if (!items.length) {
    els.feed.innerHTML = `<section class="empty-state">${icon(state.view === "reels" ? "film" : "image")}<h2>No ${state.view} yet</h2><p>Create something from Profile to start your feed.</p></section>`;
    return;
  }
  els.feed.innerHTML = items.map((item, index) => state.view === "reels" ? renderReel(item, index) : renderPost(item, index)).join("");
}

function renderPost(post, index) {
  const user = userById(post.user_id) || state.users[index % Math.max(state.users.length, 1)] || demoUsers[0];
  const username = usernameFrom(user);
  const id = post.post_id;
  const key = itemKey("post", id);
  const comments = commentsFor("post", id);
  const isOpen = state.openComments.has(key);
  const commentCount = visibleCommentCount("post", post);
  return `
    <article class="post-card">
      <header class="post-header">
        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(post.location)}</span></div>
        </div>
        <button class="icon-button" type="button" title="More">${icon("more")}</button>
      </header>
      <div class="media-frame"><img src="${escapeHtml(post.image_url)}" alt="${escapeHtml(post.caption || "Post")}" loading="lazy" /></div>
      ${renderActions("post", id)}
      <div class="post-body">
        <div class="likes">${formatCount(post.likes + (state.liked.has(String(id)) ? 1 : 0))} likes</div>
        <p class="caption"><strong>${escapeHtml(username)}</strong>${escapeHtml(post.caption || "New post")}</p>
        <button class="comments-link" data-toggle-comments="${escapeHtml(key)}" type="button">${isOpen ? "Hide" : "View all"} ${formatCount(commentCount)} comments</button>
        ${isOpen ? renderCommentList(comments) : ""}
        <button class="time-link" type="button">Just now</button>
      </div>
      <form class="comment-row" data-comment-form data-type="post" data-id="${escapeHtml(id)}">
        <input type="text" placeholder="Add a comment..." />
        <button type="submit">Post</button>
      </form>
    </article>
  `;
}

function renderReel(reel, index) {
  const user = userById(reel.user_id) || state.users[index % Math.max(state.users.length, 1)] || demoUsers[0];
  const username = usernameFrom(user);
  const id = reel.reel_id;
  const key = itemKey("reel", id);
  const comments = commentsFor("reel", id);
  const isOpen = state.openComments.has(key);
  const commentCount = visibleCommentCount("reel", reel);
  return `
    <article class="reel-card">
      <header class="reel-header">
        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(reel.location)}</span></div>
        </div>
        <button class="icon-button" type="button" title="More">${icon("more")}</button>
      </header>
      <div class="media-frame wide"><video src="${escapeHtml(reel.video_url)}" poster="${escapeHtml(reel.image_url)}" controls muted playsinline preload="metadata"></video></div>
      ${renderActions("reel", id)}
      <div class="post-body">
        <div class="likes">${formatCount(reel.likes + (state.liked.has(String(id)) ? 1 : 0))} likes</div>
        <p class="caption"><strong>${escapeHtml(username)}</strong>${escapeHtml(reel.caption || "New reel")}</p>
        <button class="comments-link" data-toggle-comments="${escapeHtml(key)}" type="button">${isOpen ? "Hide" : "View all"} ${formatCount(commentCount)} comments</button>
        ${isOpen ? renderCommentList(comments) : ""}
        <button class="time-link" type="button">Just now</button>
      </div>
      <form class="comment-row" data-comment-form data-type="reel" data-id="${escapeHtml(id)}">
        <input type="text" placeholder="Add a comment..." />
        <button type="submit">Post</button>
      </form>
    </article>
  `;
}

function renderActions(type, id) {
  const key = String(id);
  const savedKey = itemKey(type, id);
  const canDelete = state.isAdmin && Number.isInteger(Number(id));
  return `
    <div class="post-actions">
      <div class="action-group">
        <button class="icon-button ${state.liked.has(key) ? "liked" : ""}" data-like="${escapeHtml(id)}" data-type="${type}" type="button" title="Like">${icon("heart")}</button>
        <button class="icon-button" type="button" title="Comment">${icon("message")}</button>
      </div>
      <div class="action-group">
        ${canDelete ? `<button class="icon-button" data-delete="${escapeHtml(id)}" data-type="${type}" type="button" title="Delete">${icon("trash")}</button>` : ""}
        <button class="icon-button ${state.saved.has(savedKey) ? "active" : ""}" data-save="${escapeHtml(id)}" data-type="${type}" type="button" title="Save">${icon("bookmark")}</button>
      </div>
    </div>
  `;
}

function renderCommentList(comments) {
  if (!comments.length) {
    return `<div class="comment-list"><p class="muted-copy">No visible comments yet.</p></div>`;
  }
  return `
    <div class="comment-list">
      ${comments.map((comment) => `<p><strong>${escapeHtml(comment.username)}</strong>${escapeHtml(comment.text)}</p>`).join("")}
    </div>
  `;
}

function renderProfile() {
  const user = currentUser();
  const username = usernameFrom(user);
  const initials = initialsFrom(username);
  document.querySelectorAll("#navAvatar, #bottomAvatar, #mobileNavAvatar").forEach((avatar) => {
    avatar.textContent = initials;
  });
  els.profileView.innerHTML = `
    <div class="profile-page">
      <section class="profile-hero">
        <span class="account-avatar large">${escapeHtml(initials)}</span>
        <div>
          <h2>${escapeHtml(username)}</h2>
          <p>${escapeHtml(user.email || "No email available")}</p>
          <p class="profile-bio">Bio: Building moments, posts, and reels in this Instagram-style app.</p>
          <div class="profile-stats">
            <span><strong>${state.posts.filter((post) => String(post.user_id) === String(user.user_id)).length}</strong> posts</span>
            <span><strong>${state.reels.filter((reel) => String(reel.user_id) === String(user.user_id)).length}</strong> reels</span>
            <span><strong>${user.status || "active"}</strong> status</span>
          </div>
        </div>
      </section>

      <section class="profile-grid">
        <div class="tool-panel">
          <div class="section-title"><span>Switch account</span><button class="text-button" id="profileSwitchButton" type="button">Use</button></div>
          <select id="profileUserSelect">${state.users.map((item) => `<option value="${escapeHtml(item.user_id)}" ${String(item.user_id) === String(state.currentUserId) ? "selected" : ""}>${escapeHtml(usernameFrom(item))} (${escapeHtml(item.email || item.user_id)})</option>`).join("")}</select>
        </div>

        <div class="tool-panel">
          <div class="section-title"><span>Create account</span></div>
          <form id="profileCreateUserForm" class="stacked-form">
            <input id="profileNewUserEmail" type="email" placeholder="Email" required />
            <input id="profileNewUserPassword" type="password" placeholder="Password" required />
            <button class="primary-button" type="submit">Create account</button>
          </form>
        </div>

        <div class="tool-panel">
          <div class="section-title"><span>Create content</span></div>
          <button class="primary-button" id="profileOpenCreate" type="button">Create post or reel</button>
        </div>
      </section>
    </div>
  `;
}

async function renderAdmin() {
  if (!state.isAdmin) {
    els.adminView.innerHTML = `<section class="empty-state">${icon("shield")}<h2>Admin login required</h2><p>Log out and sign in with admin mode to manage users and content.</p></section>`;
    return;
  }
  try {
    const [users, roles] = await Promise.all([api("/admin/users/"), api("/admin/roles/")]);
    state.adminUsers = users;
    state.roles = roles;
  } catch (error) {
    els.adminView.innerHTML = `<section class="empty-state">${icon("shield")}<h2>Admin data unavailable</h2><p>${escapeHtml(error.message)}</p></section>`;
    return;
  }
  els.adminView.innerHTML = `
    <div class="admin-page">
      <section class="admin-header">
        <h2>Admin dashboard</h2>
        <p>Manage users, posts, reels, and roles.</p>
      </section>
      <section class="admin-grid">
        <div class="tool-panel">
          <div class="section-title"><span>User management</span><button class="text-button" data-admin-refresh type="button">Refresh</button></div>
          <div class="admin-list">
            ${state.adminUsers.map((user) => `
              <div class="admin-row">
                <span class="suggestion-avatar">${escapeHtml(initialsFrom(usernameFrom(user)))}</span>
                <div><strong>${escapeHtml(usernameFrom(user))}</strong><span>${escapeHtml(user.email || "")} · ${escapeHtml(user.status || "")}</span></div>
                <button class="text-button danger" data-admin-delete-user="${escapeHtml(user.user_id)}" type="button">Delete</button>
              </div>
            `).join("")}
          </div>
        </div>
        <div class="tool-panel">
          <div class="section-title"><span>Content moderation</span></div>
          <p class="muted-copy">Admin delete buttons are visible on real posts and reels in the feed.</p>
          <button class="primary-button" data-nav="posts" type="button">Review posts</button>
          <button class="secondary-action" data-nav="reels" type="button">Review reels</button>
        </div>
        <div class="tool-panel">
          <div class="section-title"><span>Roles</span></div>
          <div class="admin-list">
            ${state.roles.map((role) => `<div class="admin-row"><div><strong>${escapeHtml(role.role_name)}</strong><span>${escapeHtml(role.description || "No description")}</span></div></div>`).join("") || "<p class=\"muted-copy\">No roles found.</p>"}
          </div>
        </div>
      </section>
    </div>
  `;
}

function renderSaved() {
  const savedItems = Array.from(state.saved).map(findSavedItem).filter(Boolean);
  if (!savedItems.length) {
    els.savedView.innerHTML = `
      <section class="empty-state">
        ${icon("bookmark")}
        <h2>No saved posts or reels</h2>
        <p>Tap the save icon on a post or reel and it will appear here.</p>
      </section>
    `;
    return;
  }
  els.savedView.innerHTML = `
    <div class="saved-page">
      <section class="admin-header">
        <h2>Saved</h2>
        <p>Your saved posts and reels for the current session.</p>
      </section>
      <div class="saved-grid">
        ${savedItems.map(({ type, item }) => `
          <article class="saved-tile" data-nav="${type === "reel" ? "reels" : "posts"}">
            <div class="saved-media">
              ${type === "reel"
                ? `<video src="${escapeHtml(item.video_url)}" poster="${escapeHtml(item.image_url)}" muted playsinline></video>`
                : `<img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.caption || "Saved post")}" />`}
            </div>
            <div>
              <strong>${type === "reel" ? "Reel" : "Post"}</strong>
              <p>${escapeHtml(item.caption || "")}</p>
            </div>
          </article>
        `).join("")}
      </div>
    </div>
  `;
}

function formatCount(value) {
  return new Intl.NumberFormat("en", { notation: value >= 10000 ? "compact" : "standard", maximumFractionDigits: 1 }).format(value || 0);
}

function itemKey(type, id) {
  return `${type}:${id}`;
}

function commentsFor(type, id) {
  return state.commentStore.get(itemKey(type, id)) || [];
}

function visibleCommentCount(type, item) {
  return (item.comments || 0) + commentsFor(type, type === "reel" ? item.reel_id : item.post_id).length;
}

function findSavedItem(key) {
  const [type, id] = key.split(":");
  const list = type === "reel" ? state.reels : state.posts;
  const item = list.find((entry) => String(type === "reel" ? entry.reel_id : entry.post_id) === id);
  return item ? { type, item } : null;
}

function setNav(nav) {
  state.activeNav = nav;
  document.querySelectorAll("[data-nav]").forEach((button) => button.classList.toggle("active", button.dataset.nav === nav));
  els.feedView.classList.toggle("is-hidden", !["home", "posts", "reels"].includes(nav));
  els.profileView.classList.toggle("is-hidden", nav !== "profile");
  els.savedView.classList.toggle("is-hidden", nav !== "saved");
  els.adminView.classList.toggle("is-hidden", nav !== "admin");
  if (nav === "posts") setView("posts");
  if (nav === "reels") setView("reels");
  if (nav === "profile") renderProfile();
  if (nav === "saved") renderSaved();
  if (nav === "admin") renderAdmin();
}

function setView(view) {
  state.view = view;
  document.querySelectorAll("[data-view-button]").forEach((button) => button.classList.toggle("active", button.dataset.viewButton === view));
  renderFeed();
}

function openCreate() {
  if (typeof els.createDialog.showModal === "function") els.createDialog.showModal();
  else els.createDialog.setAttribute("open", "");
}

function closeCreate() {
  els.createDialog.close();
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2600);
}

async function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function createUser(email, password) {
  const user = await api("/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role_id: 1, email, password, status: "active" })
  });
  state.users.unshift(user);
  state.currentUserId = user.user_id;
  localStorage.setItem(USER_KEY, user.user_id);
  return user;
}

async function createPost(event) {
  event.preventDefault();
  const caption = document.getElementById("newPostCaption").value.trim();
  if (!caption || !state.selectedPhotoDataUrl) {
    showToast("Choose a photo and caption.");
    return;
  }
  try {
    const post = await api("/posts/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(state.currentUserId), caption, status: "active" })
    });
    const enriched = enrichPosts([{ ...post, image_url: state.selectedPhotoDataUrl }])[0];
    state.posts.unshift(enriched);
    if (Number.isInteger(Number(post.post_id))) {
      api(`/posts/${post.post_id}/media`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ post_id: post.post_id, media_url: state.selectedPhotoDataUrl, media_type: "image", order_index: 1 })
      }).catch(() => {});
    }
    showToast("Post shared.");
  } catch {
    state.posts.unshift(enrichPosts([{ post_id: `local-post-${Date.now()}`, user_id: state.currentUserId, caption, image_url: state.selectedPhotoDataUrl }])[0]);
    showToast("Post added locally.");
  }
  state.selectedPhotoDataUrl = "";
  els.createPostForm.reset();
  resetPhotoPreview();
  closeCreate();
  setNav("posts");
}

async function createReel(event) {
  event.preventDefault();
  const caption = document.getElementById("newReelCaption").value.trim();
  if (!state.selectedVideoDataUrl || !caption) {
    showToast("Choose a video and caption.");
    return;
  }
  try {
    const reel = await api("/reels/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: Number(state.currentUserId), video_url: state.selectedVideoDataUrl, caption, status: "active" })
    });
    state.reels.unshift(enrichReels([reel])[0]);
    showToast("Reel published.");
  } catch {
    state.reels.unshift(enrichReels([{ reel_id: `local-reel-${Date.now()}`, user_id: state.currentUserId, video_url: state.selectedVideoDataUrl, caption }])[0]);
    showToast("Reel added locally.");
  }
  state.selectedVideoDataUrl = "";
  els.createReelForm.reset();
  resetVideoPreview();
  closeCreate();
  setNav("reels");
}

function resetPhotoPreview() {
  els.postPhotoPreview.innerHTML = `<span data-icon="image"></span><strong>Choose a photo</strong><small>Preview before sharing</small>`;
  hydrateIcons(els.postPhotoPreview);
}

function resetVideoPreview() {
  els.reelVideoPreview.innerHTML = `<span data-icon="film"></span><strong>Choose a video</strong><small>Upload from your computer</small>`;
  hydrateIcons(els.reelVideoPreview);
}

async function deleteItem(type, id) {
  try {
    await api(type === "reel" ? `/reels/${id}` : `/posts/${id}`, { method: "DELETE" });
    if (type === "reel") state.reels = state.reels.filter((item) => String(item.reel_id) !== String(id));
    else state.posts = state.posts.filter((item) => String(item.post_id) !== String(id));
    renderFeed();
    showToast("Deleted.");
  } catch (error) {
    showToast(error.message);
  }
}

async function toggleLike(button) {
  const key = String(button.dataset.like);
  const type = button.dataset.type;
  const wasLiked = state.liked.has(key);
  const userId = Number(state.currentUserId);
  const itemId = Number(key);
  if (Number.isInteger(userId) && Number.isInteger(itemId)) {
    const base = type === "reel" ? `/reels/${itemId}/likes` : `/posts/${itemId}/likes`;
    try {
      await api(wasLiked ? `${base}/${userId}` : `${base}?user_id=${userId}`, { method: wasLiked ? "DELETE" : "POST" });
    } catch (error) {
      showToast(error.message);
      return;
    }
  }
  wasLiked ? state.liked.delete(key) : state.liked.add(key);
  renderFeed();
}

async function submitComment(form) {
  const input = form.querySelector("input");
  const text = input.value.trim();
  if (!text) return;
  const type = form.dataset.type;
  const itemId = Number(form.dataset.id);
  const userId = Number(state.currentUserId);
  if (Number.isInteger(userId) && Number.isInteger(itemId)) {
    const path = type === "reel" ? `/reels/${itemId}/comments` : `/posts/${itemId}/comments`;
    const body = type === "reel" ? { reel_id: itemId, user_id: userId, text } : { post_id: itemId, user_id: userId, text };
    try {
      await api(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    } catch (error) {
      showToast(error.message);
      return;
    }
  }
  const key = itemKey(type, form.dataset.id);
  const comments = state.commentStore.get(key) || [];
  comments.push({ username: usernameFrom(currentUser()), text });
  state.commentStore.set(key, comments);
  state.openComments.add(key);
  input.value = "";
  renderFeed();
  showToast("Comment posted.");
}

async function bootApp() {
  els.loginScreen.classList.add("is-hidden");
  els.appShell.classList.remove("is-hidden");
  els.adminNavItem.classList.toggle("is-hidden", !state.isAdmin);
  await loadUsers();
  await loadFeed();
  renderStories();
  renderFeed();
  renderProfile();
  hydrateIcons();
  setNav(state.isAdmin ? "admin" : "home");
}

document.addEventListener("click", async (event) => {
  const navButton = event.target.closest("[data-nav]");
  if (navButton) setNav(navButton.dataset.nav);
  if (event.target.closest("#logoutButton, #mobileLogoutButton")) logout();
  if (event.target.closest("#profileOpenCreate")) openCreate();
  if (event.target.closest("#closeCreateModal")) closeCreate();
  if (event.target.closest("[data-view-button]")) setView(event.target.closest("[data-view-button]").dataset.viewButton);
  const commentsButton = event.target.closest("[data-toggle-comments]");
  if (commentsButton) {
    const key = commentsButton.dataset.toggleComments;
    state.openComments.has(key) ? state.openComments.delete(key) : state.openComments.add(key);
    renderFeed();
  }
  const likeButton = event.target.closest("[data-like]");
  if (likeButton) toggleLike(likeButton);
  const saveButton = event.target.closest("[data-save]");
  if (saveButton) {
    const key = itemKey(saveButton.dataset.type, saveButton.dataset.save);
    state.saved.has(key) ? state.saved.delete(key) : state.saved.add(key);
    renderFeed();
    if (state.activeNav === "saved") renderSaved();
  }
  const deleteButton = event.target.closest("[data-delete]");
  if (deleteButton) deleteItem(deleteButton.dataset.type, deleteButton.dataset.delete);
  const adminDeleteUser = event.target.closest("[data-admin-delete-user]");
  if (adminDeleteUser) {
    try {
      await api(`/admin/users/${adminDeleteUser.dataset.adminDeleteUser}`, { method: "DELETE" });
      showToast("User deleted.");
      renderAdmin();
    } catch (error) {
      showToast(error.message);
    }
  }
  if (event.target.closest("[data-admin-refresh]")) renderAdmin();
});

document.addEventListener("submit", async (event) => {
  if (event.target === els.loginForm) login(event);
  if (event.target === els.quickSignupForm) quickSignup(event);
  if (event.target === els.createPostForm) createPost(event);
  if (event.target === els.createReelForm) createReel(event);
  if (event.target.matches("[data-comment-form]")) {
    event.preventDefault();
    submitComment(event.target);
  }
  if (event.target.id === "profileCreateUserForm") {
    event.preventDefault();
    try {
      await createUser(document.getElementById("profileNewUserEmail").value.trim(), document.getElementById("profileNewUserPassword").value);
      event.target.reset();
      renderProfile();
      showToast("Account created.");
    } catch (error) {
      showToast(error.message);
    }
  }
});

document.addEventListener("change", async (event) => {
  if (event.target.id === "newPostPhoto" && event.target.files[0]) {
    state.selectedPhotoDataUrl = await fileToDataUrl(event.target.files[0]);
    els.postPhotoPreview.innerHTML = `<img src="${escapeHtml(state.selectedPhotoDataUrl)}" alt="Selected post preview" /><strong>Photo selected</strong>`;
  }
  if (event.target.id === "newReelVideo" && event.target.files[0]) {
    state.selectedVideoDataUrl = await fileToDataUrl(event.target.files[0]);
    els.reelVideoPreview.innerHTML = `<video src="${escapeHtml(state.selectedVideoDataUrl)}" muted playsinline controls></video><strong>Video selected</strong>`;
  }
  if (event.target.id === "profileUserSelect") {
    state.currentUserId = event.target.value;
    localStorage.setItem(USER_KEY, state.currentUserId);
    await loadFeed();
    renderStories();
    renderFeed();
    renderProfile();
    showToast("Switched account.");
  }
});

document.querySelectorAll("[data-compose-tab]").forEach((tab) => {
  tab.addEventListener("click", () => {
    const selected = tab.dataset.composeTab;
    document.querySelectorAll("[data-compose-tab]").forEach((button) => button.classList.toggle("active", button === tab));
    document.querySelectorAll("[data-compose-panel]").forEach((panel) => panel.classList.toggle("hidden", panel.dataset.composePanel !== selected));
  });
});

els.createDialog.addEventListener("click", (event) => {
  if (event.target === els.createDialog) closeCreate();
});

async function init() {
  hydrateIcons();
  if (state.token) {
    try {
      await bootApp();
    } catch {
      logout();
    }
  }
}

init();
