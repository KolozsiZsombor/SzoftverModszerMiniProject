## 1. Objective
The goal is to develop a simple, user-friendly platform where users can share, browse, and rate jokes. Registration is required only for posting and rating, while reading and reacting to jokes can be done anonymously. Jokes will be sorted based on user ratings, and a hidden admin interface will enable platform management, including moderation and enforcement of a profanity filter.

## 2. Key Features

### 2.1. Frontend Features
1. **Homepage:**
  - Display a list of jokes, able to be sorted.
  - Pages or Scrolling. /tbd
  - Search Functionality.
  - Filter options.

2. **User registration/Accounts:**
  - Ability to create accounts
  - Registered can:
    - Upload Jokes.
    - Rate Jokes (star system or upvote/downvote). /tbd
    - Reactions (smileys, like, dislike).
    - Save favorites.
    - Manage Profile.

2. **Anonymous Browsing:**
  - Non-registered users can browse, read jokes.
  - Are encouraged to registration by prompts.

3. **Joke Submission**
  - A simple form.
  - Option to categorize jokes. (e.g Dark, Dad,One-liners)

4. **Rating System**
   - Star or upvote/downvote system.
   - Jokes with high average star rating/upvotes will rise to the top.
   - Jokes with low average star rating/downvoted will fall, but still be visible.

6. **Joke Detail Page**
  - Display joke with user ratings, comments, and reactions.
  - Comment section for users to discuss the joke.
  - Report button.

### 2.2. Backend Features

1. **Profanity/Bad Word Filter:**
  - Automatic filter to:
    - Prevent the submission of jokes containing offensive/profane content.
  - Option to report jokes, that bypass the filter.

2. **Admin Interface (Hitten):**
  - Admin login to access an exclusive dashboard.
  - Joke moderation:
    - View, or remove any joke.
    - No ability to edit joke.
    - Review reported jokes.
  - User management:
    -Ban or suspend users violating community guidelines.
    -Manage registered users.
  - Profanity filter management:
    - Adjust and update the word filter as needed.

3. **Moderation Queue:**
  - Jokes reported by users or flagged are placed in a queue.
  - Admins can approve, delete jokes if necessary.

4. **Rating Algorithm:**
  - Display jokes based on a dynamic rating system.
  - Top-rated jokes appear first on the homepage.
  - New jokes will be artificially placed higher, so every joke can be seen.

5. **Notification System**
  - Email notification to users on events:
    - Joke submission approval/rejection.
    - Comments or reactions on their joke.
    - Updates or warnings.

---

## Technical Stack

### 3.1 Frontend
  - **Framework:** HTML paired with JS for responsive interface.
  - **UI Framework:** CSS for styling.
  - **Interactivity:** Javascript for dynamic content loading.
### 3.2 Backend
  - **Server:** Python Flask/Django for API development.
  - **Database:**
    - **Primary database:** Oracle/ MySQL for stroing user profiles, jokes and ratings.
  - **User Authentication:** Traditional email/password with JWT tokens for session management.
  - **Profanity Filter:** An integrated profanity filtering library. 

### 3.3. Admin Tools
  - **Dashboard:** Use a prebuilt admin panel framework.
  - **Content Moderation:** Custom REST API endpoints for moderating flagged content and managing users.
    
---

## User flow

1. **Anonymous User:**
  - Browse jokes -> React to jokes -> Search/filter jokes -> Encouraged to register.

3. **Registered User:**
  - Browse jokes -> Submit joke -> View rating/reactions -> Rate other jokes -> Save favorites.

5. **Admin:**
  - Log into admin panel -> View reported jokes -> Approve/reject jokes -> Manage users and modify profanity filter.

---

## 5. Security and Scalability 

### 5.1 Security:

### 5.2 Scalability:

---

## 6. Performance and Analytics

### 6.1 Performance Optimization
  - Use lazy loarding for images and joke content.
  - Optimize database queries and indexing for faster response times.
### 6.2 Analytics and User Insights:
  - Admin acces to user reports, high-rated jokes, active users.
---

## 7 Timeline and Milestones

1. ** Week 1-2:** Initial Planning
   - Creation of Functional Specification.
   - Creation of Requirement Specification.
   - Creation of System Plan.
2. ** Week 3** Development
   - Backend API, database architecture.
   - Profanity Filter.
   - Fronted development with registration, joke submission and rating.
   - Admin dashboard, moderation tools, and users management.
3. ** Week 4** Testing
   - User testing.
   - Bug fixes.
   - Final deployment

---

## 8. Post-Launch Consideration

1. Continuous profanity filter updates based on user feedback.
2. Regular moderation of user-submitted content.
3. Launching new features like user leaderboards, joke competitions, or joke categories based on user engagement.

---
