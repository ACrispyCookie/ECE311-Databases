INSERT INTO `Departments` (`departmentTitle`, `departmentCode`) VALUES ('ece', '123');
INSERT INTO `Courses` (`courseTitle`, `courseCode`, `courseId`, `departmentCode`) VALUES ('prog 1', 'ece115', '635f68f5-d291-11ef-a0b1-0242ac140004', '123');
INSERT INTO `Categories` (`title`, `courseId`) VALUES ('labs', '635f68f5-d291-11ef-a0b1-0242ac140004');
INSERT INTO `Users` (`username`, `id`, `departmentCode`) VALUES ('jason', '1', '123');
INSERT INTO `Users` (`username`, `id`, `departmentCode`) VALUES ('tsiantosd', '2', '123');
INSERT INTO `Posts` (`url`, `title`, `createdAt`, `id`, `userId`, `categoryTitle`, `courseId`) VALUES ('test', 'hello', '2025-01-14 18:07:01', '1', '1', 'labs', '635f68f5-d291-11ef-a0b1-0242ac140004');
INSERT INTO `Reactions` (`upvote`, `userId`, `postId`) VALUES ('1', '1', '1');