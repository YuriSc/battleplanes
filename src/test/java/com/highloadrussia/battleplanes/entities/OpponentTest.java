package com.highloadrussia.battleplanes.entities;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

public class OpponentTest {
    @Test
    public void testConstructor() {
        GameField gameField = new GameField(1, 1);
        Opponent actualOpponent = new Opponent(3, gameField, new Player(new GameField(1, 1)));
        assertEquals(5, actualOpponent.getWidth());
        assertEquals(3, actualOpponent.getY());
        assertEquals(1, actualOpponent.getX());
        assertEquals(3, actualOpponent.getHeight());
        assertFalse(actualOpponent.isReadyToShoot());
        assertSame(gameField, actualOpponent.getGameField());
        assertFalse(actualOpponent.isMarkedToRemove());
    }

    @Test
    public void testSetReadyToShoot() {
        GameField gameField = new GameField(1, 1);
        Opponent opponent = new Opponent(3, gameField, new Player(new GameField(1, 1)));
        opponent.setReadyToShoot(true);
        assertTrue(opponent.isReadyToShoot());
    }

    @Test
    public void testMove() {
        GameField gameField = new GameField(0, 1);
        Opponent opponent = new Opponent(3, gameField, new Player(new GameField(1, 1)));
        opponent.move();
        assertTrue(opponent.isMarkedToRemove());
    }
}
