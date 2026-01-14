# Task Section - Quick Start Guide

## 🚀 Getting Started

### 1. Migrate Existing Data (If Needed)

If you have existing tasks in the database with old format values:

```bash
cd office-mate-backend
python migrate_task_values.py
```

This will convert:

- `Todo` → `pending`
- `InProgress` → `in_progress`
- `Done` → `completed`
- `Low` → `low`
- `Medium` → `medium`
- `High` → `high`
- `Urgent` → `urgent`

### 2. Start the Backend

```bash
cd office-mate-backend
python flask_app.py
```

Server will start on http://localhost:5001

### 3. Start the Frontend

```bash
cd office-mate
npm run dev
```

Frontend will start on http://localhost:8081

### 4. Run Tests (Optional)

```bash
cd office-mate-backend
python test_task_api_complete.py
```

## 📋 How to Use

### Creating Tasks

#### From the Tasks Page:

1. Navigate to `/tasks`
2. Click "Add Task" button
3. Fill in:
   - **Title** (required)
   - Description
   - **Priority**: low, medium, high, urgent
   - **Status**: pending, in_progress, completed
   - **Due Date**: Select from calendar
   - **Linked Document**: Select a document (optional)
4. Click "Save"

#### From a Document:

1. View a document in the Documents page
2. Click "Create Task" in the document sidebar
3. The document will be automatically linked
4. Fill in task details and save

### Viewing Tasks

Tasks are automatically grouped into:

- **Overdue** - Past due date, not completed (red border)
- **Today** - Due today (yellow border)
- **Upcoming** - Due in the future
- **Completed** - Finished tasks (green border)

### Quick Actions

- **Toggle Status**: Click the checkbox icon to mark pending → completed
- **Edit Task**: Click the pencil icon
- **Delete Task**: Click the trash icon

### Filtering Tasks

Use the filter dropdown to show:

- All tasks
- Only pending
- Only in progress
- Only completed

### Dashboard Integration

The Dashboard shows:

- **Open Tasks Count** - Total pending + in_progress
- **Upcoming Deadlines** - Tasks due in next 7 days
- **High Priority Tasks** - Urgent tasks requiring attention

## 🌐 Bilingual Support

To switch language:

1. Click the language toggle in the navigation bar
2. All task labels will update to Sinhala or English

**Centralized Strings:**
All labels use `t('tasks.pending')` format, making translation easy.

## 🔗 Linking Tasks to Documents

### Why Link Tasks?

- Track follow-up actions for specific documents
- See all tasks related to a contract, invoice, or report
- Better context when reviewing tasks

### How It Works:

1. When creating a task, select a document from the dropdown
2. The document name will appear as a badge on the task
3. Filter tasks by document using the API: `GET /api/tasks?document_id=5`

## 📊 API Quick Reference

### Create Task

```bash
curl -X POST http://localhost:5001/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review contract",
    "priority": "high",
    "due_date": "2026-01-20",
    "document_id": 5
  }'
```

### Get All Tasks

```bash
curl -X GET "http://localhost:5001/api/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Filter by Status

```bash
curl -X GET "http://localhost:5001/api/tasks?status=pending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Task

```bash
curl -X PATCH http://localhost:5001/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete Task

```bash
curl -X DELETE http://localhost:5001/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Upcoming Tasks

```bash
curl -X GET "http://localhost:5001/api/tasks/upcoming?days=3" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐛 Troubleshooting

### Tasks Not Showing

1. Check browser console for errors
2. Verify Flask server is running on port 5001
3. Check JWT token is valid (login again)
4. Check Network tab in DevTools for API responses

### Status/Priority Not Updating

1. Ensure you're using lowercase values: `pending`, not `Pending`
2. Check backend logs for validation errors
3. Run migration script if using old data format

### Document Linking Not Working

1. Verify document exists and belongs to current user
2. Check document ID is a valid integer
3. Backend validates document ownership before linking

### CORS Errors

1. Check Flask app has CORS enabled for localhost:8081
2. Verify `supports_credentials=True` in CORS config
3. Restart Flask server after config changes

## ✅ Testing Checklist

- [ ] Create a task without document link
- [ ] Create a task with document link
- [ ] Edit task title and description
- [ ] Change task priority
- [ ] Change task status via form
- [ ] Toggle status via checkbox
- [ ] Delete a task
- [ ] Filter by status
- [ ] Check overdue section shows past due tasks
- [ ] Check today section shows tasks due today
- [ ] Check upcoming section shows future tasks
- [ ] Check Dashboard shows upcoming deadlines
- [ ] Switch language and verify translations
- [ ] Create task from document context

## 📝 Report Requirements Checklist

All requirements from the specification are implemented:

- [x] Users can create, update, and track tasks
- [x] Tasks linked to specific documents
- [x] Priority levels (low, medium, high, urgent)
- [x] Due date support
- [x] Status tracking (pending, in_progress, completed)
- [x] Reminders for upcoming deadlines
- [x] Bilingual support (Sinhala-English)
- [x] Better task visibility than manual methods
- [x] Integration with document organizer

## 🎯 Next Steps

1. **Production Deployment:**
   - Update `SECRET_KEY` in flask_app.py
   - Use PostgreSQL instead of SQLite
   - Add proper HTTPS
   - Configure production CORS origins

2. **Enhancements:**
   - Email notifications for overdue tasks
   - Task assignment to other users
   - Recurring tasks
   - Task templates
   - Export tasks to CSV
   - Task comments/notes

3. **Mobile Support:**
   - Add responsive breakpoints for mobile
   - Consider PWA for offline support
   - Push notifications for deadlines

## 💡 Tips

- Use **high priority** for urgent matters requiring immediate attention
- Set **realistic due dates** to avoid constant overdue tasks
- **Link tasks to documents** for better context
- **Complete tasks promptly** to keep the dashboard clean
- Review **upcoming deadlines** daily on the Dashboard
- Use the **filter** to focus on specific task categories

## 📞 Support

If you encounter issues:

1. Check [TASK_SECTION_FIX_SUMMARY.md](./TASK_SECTION_FIX_SUMMARY.md) for detailed technical documentation
2. Review Flask server logs for backend errors
3. Check browser console for frontend errors
4. Run the test script to verify API functionality

---

**Happy Task Management! 🎉**
