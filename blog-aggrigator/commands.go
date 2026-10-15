package main

import (
	"errors"
)

type command struct {
	cmd  string
	args []string
}

type commands struct {
	cmds map[string]func(*state, command) error
}

func (c *commands) run(s *state, cmd command) error {
	value, ok := c.cmds[cmd.cmd]
	if !ok {
		return errors.New("Command not found:")
	}
	err := value(s, cmd)
	if err != nil {
		return err
	}
	return nil
}

func (c *commands) register(name string, f func(*state, command) error) {
	c.cmds[name] = f

}
