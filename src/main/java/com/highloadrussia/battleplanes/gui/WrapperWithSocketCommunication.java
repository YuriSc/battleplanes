package com.highloadrussia.battleplanes.gui;

import com.highloadrussia.battleplanes.entities.Boom;
import com.highloadrussia.battleplanes.entities.Enemy;
import com.highloadrussia.battleplanes.entities.Game;
import com.highloadrussia.battleplanes.entities.MenuAction;
import com.highloadrussia.battleplanes.entities.MovableEntity;
import com.highloadrussia.battleplanes.entities.Player;
import com.highloadrussia.battleplanes.entities.PlayerAction;
import com.highloadrussia.battleplanes.services.CommandClient;
import com.highloadrussia.battleplanes.services.CommandServer;

import java.io.IOException;
import java.util.List;

public class WrapperWithSocketCommunication implements Gui {

    private final CommandClient commandClient;
    private int counter = 0;
    private final Gui target;

    public WrapperWithSocketCommunication(Gui target, CommandClient commandClient) {
        this.commandClient = commandClient;
        this.target = target;
    }

    @Override
    public int getHeightInRows() {
        return target.getHeightInRows();
    }

    @Override
    public int getWidthInColumns() {
        return target.getWidthInColumns();
    }

    @Override
    public void init() throws IOException {
        target.init();
    }

    @Override
    public void drawPlayer(Player player) {
        target.drawPlayer(player);
    }

    @Override
    public void drawEnemies(List<Enemy> enemies) {
        target.drawEnemies(enemies);
    }

    @Override
    public void drawBullets(List<MovableEntity> bullets) {
        target.drawBullets(bullets);
    }

    @Override
    public void drawBooms(List<Boom> booms) {
        target.drawBooms(booms);
    }

    @Override
    public void drawLife(Player player) throws IOException {
        target.drawLife(player);
    }

    @Override
    public void drawDistance(Player player) throws IOException {
        target.drawDistance(player);
    }

    @Override
    public void drawMenu() throws IOException {
        target.drawMenu();
    }

    @Override
    public void drawGameOver(long distance) throws IOException {
        target.drawGameOver(distance);
    }

    @Override
    public PlayerAction pullPlayerAction() throws IOException {
        return commandClient.getPlayerAction();
    }

    @Override
    public MenuAction pullMenuAction() throws IOException {
        if (commandClient.isClientConnected())
            return MenuAction.START;
        return MenuAction.EXIT;
    }

    @Override
    public void redraw(Game game) throws IOException {
        commandClient.sendGameState(game);
        counter++;
        if (counter % 10 == 1) {
            target.redraw(game);
        }
    }

    @Override
    public void exit() throws IOException {
        target.exit();
        commandClient.close();
    }
}
