PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS user_tasks;
DROP TABLE IF EXISTS onboarding_tasks;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    title TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    user_type TEXT NOT NULL CHECK (user_type IN ('new_hire', 'hr_specialist', 'manager')),
    role_id INTEGER,
    manager_id INTEGER,
    mentor_id INTEGER,
    start_date TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (manager_id) REFERENCES users(id),
    FOREIGN KEY (mentor_id) REFERENCES users(id)
);

CREATE TABLE onboarding_tasks (
    id INTEGER PRIMARY KEY,
    role_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT NOT NULL CHECK (task_type IN ('learning_module', 'hr_form', 'simulated_project')),
    default_due_days INTEGER,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE user_tasks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'overdue')),
    due_date TEXT,
    completed_at TEXT,
    submission_url TEXT,
    feedback TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE (user_id, task_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES onboarding_tasks(id)
);

CREATE TABLE resources (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    description TEXT,
    resource_url TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX idx_roles_department_id ON roles(department_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_manager_id ON users(manager_id);
CREATE INDEX idx_users_mentor_id ON users(mentor_id);
CREATE INDEX idx_onboarding_tasks_role_id ON onboarding_tasks(role_id);
CREATE INDEX idx_user_tasks_user_id ON user_tasks(user_id);
CREATE INDEX idx_user_tasks_task_id ON user_tasks(task_id);
CREATE INDEX idx_user_tasks_status ON user_tasks(status);
CREATE INDEX idx_resources_category ON resources(category);