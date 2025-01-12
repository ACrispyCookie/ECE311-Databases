CREATE TABLE Users (
    username        VARCHAR(255),
    id              INTEGER NOT NULL,
    departmentCode  INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE Posts (
    url             VARCHAR(255),
    title           VARCHAR(255),
    createdAt       TIMESTAMP,
    id              INTEGER NOT NULL,
    userId          INTEGER NOT NULL,
    titleId         VARCHAR(255),
    courseId        INTEGER,
    PRIMARY KEY (id, userId)
);

CREATE TABLE Departments (
    departmentTitle VARCHAR(255),
    departmentCode  INTEGER NOT NULL,
    PRIMARY KEY (departmentCode)
);

CREATE TABLE Courses (
    courseTitle     VARCHAR(255),
    courseCode      VARCHAR(50),
    courseId        INTEGER NOT NULL,
    departmentCode  INTEGER,
    PRIMARY KEY (courseId)
);

CREATE TABLE Students (
    id              INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Admins (
    id              INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Developers (
    id              INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Categories (
    title           VARCHAR(255) NOT NULL,
    courseId        INTEGER NOT NULL,
    PRIMARY KEY (title, courseId)
);

CREATE TABLE Reactions (
    upvote          BOOLEAN,
    userId          INTEGER NOT NULL,
    postId          INTEGER NOT NULL,
    PRIMARY KEY (userId, postId)
);

CREATE TABLE Fullnames (
    firstName       VARCHAR(255) NOT NULL,
    lastName        VARCHAR(255) NOT NULL,
    userId          INTEGER NOT NULL,
    PRIMARY KEY (firstName, lastName, userId)
);

ALTER TABLE Users ADD FOREIGN KEY (departmentCode) REFERENCES Departments (departmentCode) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE Posts ADD FOREIGN KEY (titleId, courseId) REFERENCES Categories (title, courseId) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE Courses ADD FOREIGN KEY (departmentCode) REFERENCES Departments (departmentCode) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE Posts ADD FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Students ADD FOREIGN KEY (id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Admins ADD FOREIGN KEY (id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Developers ADD FOREIGN KEY (id) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Categories ADD FOREIGN KEY (courseId) REFERENCES Courses (courseId) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Reactions ADD FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Reactions ADD FOREIGN KEY (postId) REFERENCES Posts (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Fullnames ADD FOREIGN KEY (userId) REFERENCES Users (id) ON DELETE CASCADE ON UPDATE CASCADE;
