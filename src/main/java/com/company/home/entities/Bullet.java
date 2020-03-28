package com.company.home.entities;

public class Bullet extends MovableEntity {

    private final static int BULLET_HEIGHT = 1;
    private final static int BULLET_WIDTH = 1;

    public Bullet(Player player, GameField gameField) {
        super(player.getX() + 1, player.getY() + ((player.getHeight() - 1) / 2), BULLET_WIDTH, BULLET_HEIGHT, gameField);
    }

    public void move() {
        this.setX(this.getX() + 1);

        if (this.getX() == this.getGameField().getWidth()) {
            this.setMarkedToRemove();
        }
    }
}
