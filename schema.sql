-- Create students table with a name column
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,  -- Add the name column here
    class TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_codes (
    code TEXT PRIMARY KEY,
    assigned_to TEXT,
    usage_count INTEGER DEFAULT 0,
    FOREIGN KEY (assigned_to) REFERENCES students(student_id)
);
