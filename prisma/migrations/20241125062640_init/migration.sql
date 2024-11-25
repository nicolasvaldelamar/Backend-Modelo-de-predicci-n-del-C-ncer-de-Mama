-- CreateTable
CREATE TABLE `predictions` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `features` JSON NOT NULL,
    `prediction` INTEGER NOT NULL,
    `tumor_type` VARCHAR(191) NOT NULL,
    `probability` DOUBLE NOT NULL,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `model_metrics` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `accuracy` DOUBLE NOT NULL,
    `precision` DOUBLE NOT NULL,
    `recall` DOUBLE NOT NULL,
    `f1_score` DOUBLE NOT NULL,
    `total_predictions` INTEGER NOT NULL,
    `last_updated` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `feature_importance` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `feature` VARCHAR(191) NOT NULL,
    `importance` DOUBLE NOT NULL,
    `last_updated` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    UNIQUE INDEX `feature_importance_feature_key`(`feature`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
