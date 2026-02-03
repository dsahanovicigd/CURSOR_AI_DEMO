# How to Import Postman Collection

## Quick Import Steps

1. **Open Postman**
   - Launch Postman application
   - Or use Postman web version

2. **Import Collection**
   - Click **Import** button (top left)
   - Select **File** tab
   - Choose `Blogging_API_Collection.json`
   - Click **Import**

3. **Create Environment** (Optional but Recommended)
   - Click **Environments** (left sidebar)
   - Click **+** to create new environment
   - Name it: "Blogging API Local"
   - Add variable:
     - Variable: `base_url`
     - Initial Value: `http://localhost:5001`
     - Current Value: `http://localhost:5001`
   - Click **Save**
   - Select this environment from dropdown (top right)

4. **Start Testing**
   - Open collection: **Blogging Platform API**
   - Run requests in order:
     1. Register User
     2. Login (saves access_token automatically)
     3. Get All Posts
     4. Create Post
     5. etc.

## Collection Features

✅ **Auto-save Variables**: Collection automatically saves:
- `access_token` after login
- `user_id` after register/login
- `post_id` after creating/getting post
- `comment_id` after creating comment
- `category_id` after getting categories

✅ **Bearer Token Auth**: Protected requests automatically use `{{access_token}}`

✅ **Complete Coverage**: All scenarios covered:
- User authentication
- Post CRUD operations
- Comment system
- Category management
- Search functionality
- Pagination (20 per page)

## Alternative: Import via URL

If you have the collection hosted:
1. Click **Import**
2. Select **Link** tab
3. Paste collection URL
4. Click **Continue** → **Import**

## Troubleshooting

**Collection not importing?**
- Verify JSON file is valid
- Check Postman version (requires v7+)
- Try importing via File → Import

**Variables not saving?**
- Make sure you're using the collection (not individual requests)
- Check that tests are enabled in Postman settings
- Verify environment is selected

**Requests failing?**
- Check `base_url` is set correctly
- Verify backend is running on port 5001
- Check authentication token is set

---

**Ready to test!** 🚀
