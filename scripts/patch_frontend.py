import os

app_js_path = r"d:\Quandance\insta\frontend\app.js"

with open(app_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add edit button to the profile view next to delete button
content = content.replace(
    """<button class="icon-button danger" style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.5);" data-delete="${escapeHtml(item.post_id || item.reel_id)}" data-type="${item.video_url ? 'reel' : 'post'}" type="button">${icon("trash")}</button>""",
    """<button class="icon-button danger" style="position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.5);" data-delete="${escapeHtml(item.post_id || item.reel_id)}" data-type="${item.video_url ? 'reel' : 'post'}" type="button" title="Delete">${icon("trash")}</button>
                     <button class="icon-button" style="position:absolute; top:8px; right:40px; background:rgba(0,0,0,0.5);" data-edit="${escapeHtml(item.post_id || item.reel_id)}" data-type="${item.video_url ? 'reel' : 'post'}" data-caption="${escapeHtml(item.caption)}" type="button" title="Edit">E</button>"""
)

# Add event listener for edit
edit_logic = """
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
  }
"""

content = content.replace(
    "const deleteButton = event.target.closest(\"[data-delete]\");\n  if (deleteButton) deleteItem(deleteButton.dataset.type, deleteButton.dataset.delete);",
    "const deleteButton = event.target.closest(\"[data-delete]\");\n  if (deleteButton) deleteItem(deleteButton.dataset.type, deleteButton.dataset.delete);\n" + edit_logic
)

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched edit button successfully!")
