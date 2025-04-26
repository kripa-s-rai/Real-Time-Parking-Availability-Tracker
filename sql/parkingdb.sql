-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS parking;
USE parking;

-- Table for storing streaming results
CREATE TABLE IF NOT EXISTS parking_log (
    lot_id VARCHAR(10),
    window_start DATETIME,
    window_end DATETIME,
    count INT
);

-- Table for storing batch processing results
CREATE TABLE IF NOT EXISTS parking_log_batch (
    window_start DATETIME NOT NULL,
    window_end DATETIME NOT NULL,
    lot_id VARCHAR(10) NOT NULL,
    event_count INT NOT NULL,
    PRIMARY KEY (window_start, window_end, event_count)
);
