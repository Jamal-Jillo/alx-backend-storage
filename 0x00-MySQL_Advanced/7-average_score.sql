-- Create stored procedure to compute average score for a user
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE user_score FLOAT;
    SELECT AVG(score) INTO user_score FROM corrections WHERE user_id = user_id;
    UPDATE users SET average_score = user_score WHERE id = user_id;
END //
DELIMITER ;
