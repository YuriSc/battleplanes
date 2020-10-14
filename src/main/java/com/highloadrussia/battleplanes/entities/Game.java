package com.highloadrussia.battleplanes.entities;

import com.highloadrussia.battleplanes.entities.factories.EnemyFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Game {

    private int timeSlot = 0;

    private final GameField gameField;
    private final Player player;

    private final List<Enemy> enemies;
    private final List<MovableEntity> bullets;
    private final List<Boom> booms;

    public Game(int gameFieldWidthInColumns, int gameFieldHeightInColumns) {
        this.gameField = new GameField(gameFieldWidthInColumns, gameFieldHeightInColumns);
        this.player = new Player(gameField);
        this.enemies = new ArrayList<>();
        this.bullets = new ArrayList<>();
        this.booms = new ArrayList<>();
    }

    public GameField getGameField() {
        return gameField;
    }

    public Player getPlayer() {
        return player;
    }

    public List<Enemy> getEnemies() {
        return enemies;
    }

    public List<MovableEntity> getBullets() {
        return bullets;
    }

    public List<Boom> getBooms() {
        return booms;
    }

    public int getTimeSlot() {
        return timeSlot;
    }

    public void setTimeSlot(int timeSlot) {
        this.timeSlot = timeSlot;
    }

    public void move(PlayerAction playerAction) {
        doPlayerAction(playerAction);
        createEnemies();
        doEnemiesAction();
        processInteractions();
        removeDestroyed();
        moveUnits();

        timeSlot++;
    }

    private void moveUnits() {
        player.move();
        bullets.forEach(MovableEntity::move);
        enemies.forEach(MovableEntity::move);
        booms.forEach(MovableEntity::move);
    }

    private void createEnemies() {
        Enemy enemy = EnemyFactory.createEnemy(this);

        if (enemy != null) {
            enemies.add(enemy);
        }
    }

    private void doEnemiesAction() {
        enemies.stream()
                .map(Enemy::tryShoot)
                .filter(Objects::nonNull)
                .forEach(bullets::add);
    }

    private void doPlayerAction(PlayerAction playerAction) {
        PlayerBullet bullet = player.doAction(playerAction);

        if (bullet != null) {
            bullets.add(bullet);
        }
    }

    private void processInteractions() {
        bullets.forEach(bullet -> {
            enemies.stream()
                    .filter(enemy -> enemy.isIntersect(bullet) && (bullet instanceof PlayerBullet))
                    .forEach(enemy -> {
                        bullet.destroy();
                        enemy.destroy();
                        booms.add(new Boom(bullet.getX(), bullet.getY(), gameField));
                    });

            if (player.isIntersect(bullet) && (bullet instanceof EnemyBullet)) {
                bullet.destroy();
                booms.add(new Boom(bullet.getX(), bullet.getY(), gameField));
                player.decreaseLife();
            }
        });

        enemies.stream()
                .filter(enemy -> enemy.isIntersect(player))
                .forEach(enemy -> {
                    player.decreaseLife();
                    enemy.destroy();
                    booms.add(new Boom(enemy.getX(), enemy.getY(), gameField));
                });
    }

    private void removeDestroyed() {
        bullets.removeIf(MovableEntity::isDestroyed);
        enemies.removeIf(MovableEntity::isDestroyed);
        booms.removeIf(MovableEntity::isDestroyed);
    }
}