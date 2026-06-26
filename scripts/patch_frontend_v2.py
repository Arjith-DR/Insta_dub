import os
import re

app_js_path = r"d:\Quandance\insta\frontend\app.js"

with open(app_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update state
content = content.replace(
    "adminUsers: [],",
    "adminUsers: [],\n  following: new Set(),\n  followers: new Set(),"
)

# 2. Update renderActions signature and logic
content = content.replace(
    "function renderActions(type, id) {",
    "function renderActions(type, id, ownerId) {"
)
content = content.replace(
    "const canDelete = state.isAdmin && Number.isInteger(Number(id));",
    "const canDelete = state.isAdmin || (Number.isInteger(Number(id)) && String(ownerId) === String(state.currentUserId));"
)

# 3. Update callers to renderActions
content = content.replace(
    "${renderActions(\"post\", id)}",
    "${renderActions(\"post\", id, post.user_id)}"
)
content = content.replace(
    "${renderActions(\"reel\", id)}",
    "${renderActions(\"reel\", id, reel.user_id)}"
)

# 4. Add follow buttons in post/reel headers
content = content.replace(
    """        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(post.location)}</span></div>
        </div>
        <button class="icon-button" type="button" title="More">${icon("more")}</button>""",
    """        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(post.location || "Instagram")}</span></div>
        </div>
        ${String(post.user_id) !== String(state.currentUserId) ? `<button class="text-button" data-follow="${escapeHtml(post.user_id)}" type="button">${state.following.has(String(post.user_id)) ? "Following" : "Follow"}</button>` : ""}
        <button class="icon-button" type="button" title="More">${icon("more")}</button>"""
)

content = content.replace(
    """        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(reel.location)}</span></div>
        </div>
        <button class="icon-button" type="button" title="More">${icon("more")}</button>""",
    """        <div class="post-author">
          <span class="author-avatar">${escapeHtml(initialsFrom(username))}</span>
          <div class="author-meta"><strong>${escapeHtml(username)}</strong><span>${escapeHtml(reel.location || "Reels")}</span></div>
        </div>
        ${String(reel.user_id) !== String(state.currentUserId) ? `<button class="text-button" data-follow="${escapeHtml(reel.user_id)}" type="button">${state.following.has(String(reel.user_id)) ? "Following" : "Follow"}</button>` : ""}
        <button class="icon-button" type="button" title="More">${icon("more")}</button>"""
)

# 5. Add loadFollowers function and call it in loadFeed
content = content.replace(
    "async function loadFeed() {",
    """async function loadFollowers() {
  if (!state.currentUserId || state.usingDemo) return;
  try {
    const [followingList, followersList] = await Promise.all([
      api(`/followers/following/${state.currentUserId}`),
      api(`/followers/${state.currentUserId}`)
    ]);
    state.following = new Set(followingList.map(f => String(f.following_id)));
    state.followers = new Set(followersList.map(f => String(f.follower_id)));
  } catch (e) {
    console.error("Failed to load followers", e);
  }
}

async function loadFeed() {
  await loadFollowers();"""
)

# 6. Add Follow toggle logic and attach it
content = content.replace(
    "async function submitComment",
    """async function toggleFollow(targetUserId) {
  targetUserId = String(targetUserId);
  const isFollowing = state.following.has(targetUserId);
  const currentUserId = Number(state.currentUserId);
  if (!Number.isInteger(currentUserId)) return;
  
  try {
    if (isFollowing) {
      await api(`/followers/${currentUserId}/${targetUserId}`, { method: "DELETE" });
      state.following.delete(targetUserId);
    } else {
      await api(`/followers/?follower_id=${currentUserId}&following_id=${targetUserId}`, { method: "POST" });
      state.following.add(targetUserId);
    }
    renderFeed();
    if (state.activeNav === "profile") renderProfile();
  } catch (e) {
    showToast(e.message);
  }
}

async function submitComment"""
)

content = content.replace(
    "const deleteButton = event.target.closest(\"[data-delete]\");",
    """const followButton = event.target.closest("[data-follow]");
  if (followButton) toggleFollow(followButton.dataset.follow);
  const deleteButton = event.target.closest("[data-delete]");"""
)

content = content.replace(
    "const deleteButton = event.target.closest(\"[data-delete]\");\n  if (deleteButton) deleteItem(deleteButton.dataset.type, deleteButton.dataset.delete);",
    """const deleteButton = event.target.closest("[data-delete]");
  if (deleteButton) deleteItem(deleteButton.dataset.type, deleteButton.dataset.delete);
  
  const editButton = event.target.closest("[data-edit]");
  if (editButton) {
    const id = editButton.dataset.edit;
    const type = editButton.dataset.type;
    const oldCaption = editButton.dataset.caption;
    const newCaption = prompt("Edit caption:", oldCaption);
    if (newCaption !== null && newCaption.trim() !== "") {
       try {
         await api(`/${type === 'reel' ? 'reels' : 'posts'}/${id}?new_caption=${encodeURIComponent(newCaption)}`, { method: "PUT" });
         showToast("Updated!");
         await loadFeed();
         renderProfile();
         renderFeed();
       } catch (e) {
         showToast(e.message);
       }
    }
  }"""
)


# 7. Update renderProfile safely! We only replace the exact function by extracting it!
start_idx = content.find("function renderProfile() {")
# We'll find the next function which is usually `function renderStories() {` or similar.
# Since we know `renderStories` is immediately after, let's look for it:
end_idx = content.find("function renderStories() {")
if start_idx != -1 and end_idx != -1:
    new_render_profile = """function renderProfile() {
  const user = currentUser();
  const username = usernameFrom(user);
  const initials = initialsFrom(username);
  document.querySelectorAll("#navAvatar, #bottomAvatar, #mobileNavAvatar").forEach((avatar) => {
    avatar.textContent = initials;
  });
  
  const myPosts = state.posts.filter((post) => String(post.user_id) === String(user.user_id));
  const myReels = state.reels.filter((reel) => String(reel.user_id) === String(user.user_id));
  
  els.profileView.innerHTML = `
    <div class="profile-page">
      <section class="profile-hero">
        <span class="account-avatar large">${escapeHtml(initials)}</span>
        <div>
          <h2>${escapeHtml(username)}</h2>
          <p>${escapeHtml(user.email || "No email available")}</p>
          <div class="profile-stats">
            <span><strong>${myPosts.length}</strong> posts</span>
            <span><strong>${myReels.length}</strong> reels</span>
            <span><strong>${state.followers.size}</strong> followers</span>
            <span><strong>${state.following.size}</strong> following</span>
          </div>
        </div>
      </section>

      <section class="profile-grid">
        <div class="tool-panel">
          <div class="section-title"><span>Profile Settings</span></div>
          <form id="updateProfileForm" class="stacked-form">
            <input id="profileUpdateUsername" type="text" placeholder="New username" />
            <input id="profileUpdateBio" type="text" placeholder="Update bio" />
            <select id="profileUpdatePrivacy">
               <option value="public">Public</option>
               <option value="private">Private</option>
            </select>
            <button class="primary-button" type="submit">Update Profile</button>
          </form>
        </div>
        
        <div class="tool-panel" style="grid-column: 1 / -1;">
          <div class="section-title"><span>Your Content</span></div>
          <div class="feed-switch" role="tablist">
            <button class="switch-button active" type="button">Posts & Reels</button>
          </div>
          <div class="saved-grid">
             ${[...myPosts, ...myReels].map(item => `
               <article class="saved-tile">
                  <div class="saved-media" style="position:relative;">
                     ${item.video_url 
                       ? `<video src="${escapeHtml(item.video_url)}" muted playsinline></video>` 
                       : `<img src="${escapeHtml(item.image_url)}" />`}
                     <button class="icon-button danger" style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.5);" data-delete="${escapeHtml(item.post_id || item.reel_id)}" data-type="${item.video_url ? 'reel' : 'post'}" type="button" title="Delete">${icon("trash")}</button>
                     <button class="icon-button" style="position:absolute; top:8px; right:40px; background:rgba(0,0,0,0.5);" data-edit="${escapeHtml(item.post_id || item.reel_id)}" data-type="${item.video_url ? 'reel' : 'post'}" data-caption="${escapeHtml(item.caption)}" type="button" title="Edit">E</button>
                  </div>
               </article>
             `).join("")}
             ${(myPosts.length === 0 && myReels.length === 0) ? '<p class="muted-copy">You haven\\'t posted anything yet.</p>' : ''}
          </div>
        </div>

        <div class="tool-panel">
          <div class="section-title"><span>Switch account</span><button class="text-button" id="profileSwitchButton" type="button">Use</button></div>
          <select id="profileUserSelect">${state.users.map((item) => `<option value="${escapeHtml(item.user_id)}" ${String(item.user_id) === String(state.currentUserId) ? "selected" : ""}>${escapeHtml(usernameFrom(item))} (${escapeHtml(item.email || item.user_id)})</option>`).join("")}</select>
        </div>
      </section>
    </div>
  `;
}

"""
    content = content[:start_idx] + new_render_profile + content[end_idx:]


# Handle update profile submit
content = content.replace(
    "if (event.target.id === \"profileCreateUserForm\") {",
    """if (event.target.id === "updateProfileForm") {
    event.preventDefault();
    const username = document.getElementById("profileUpdateUsername").value.trim();
    const bio = document.getElementById("profileUpdateBio").value.trim();
    const privacy = document.getElementById("profileUpdatePrivacy").value;
    
    try {
      if (username) {
         await api(`/users/${state.currentUserId}/username?new_username=${encodeURIComponent(username)}`, { method: "PUT" });
      }
      if (bio) {
         await api(`/bios/`, { 
            method: "POST", 
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({user_id: Number(state.currentUserId), b_txt: bio, current: true}) 
         });
      }
      await api(`/privacy/${state.currentUserId}?priv_status=${privacy}`, { method: "PUT" });
      
      showToast("Profile updated!");
      await loadUsers(); // refresh username
      renderProfile();
      renderFeed(); // feed names might update
    } catch(e) {
      showToast(e.message);
    }
  }

  if (event.target.id === "profileCreateUserForm") {"""
)

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched app.js safely!")
