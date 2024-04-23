CREATE TABLE User(
    email varchar(50),
    last_name varchar(50) NOT NULL,
    first_name varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
    
    password varchar(32) NOT NULL,
    primary key(email)
);

CREATE TABLE Tasks(
    task_id int,
    email varchar(50),
    task_name varchar(50) NOT NULL,
    task_desc varchar(255) NOT NULL,
    deadline DATE NOT NULL,
    importance int NOT NULL,
    is_complete BIT(1),
    completion_date DATE NOT NULL,
    foreign key(email) references User(email),
    primary key(task_id,email)
);

CREATE TABLE Feedback(
    email varchar(50),
    task_id int,
    rating numeric(1,0) NOT NULL,
    comment varchar(255),
    foreign key(email) references User(email),
    foreign key(task_id) references Tasks(task_id),
    primary key(task_id,email)
);

CREATE TABLE Work_Session(
    session_id int,
    email varchar(50),
    task_id int,
    technique varchar(50) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    foreign key(email) references User(email),
    foreign key(task_id) references Tasks(task_id),
    primary key(session_id,email,task_id)
);

CREATE TABLE Admin(
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    branch varchar(50) NOT NULL,
    primary key(username)
);