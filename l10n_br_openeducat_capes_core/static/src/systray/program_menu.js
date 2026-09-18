/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class ProgramMenu extends Component {
    static template = "l10n_br_openeducat_capes_core.ProgramMenu";
    static components = { Dropdown, DropdownItem };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            currentProgram: session.current_program || null,
            allowedPrograms: session.allowed_programs || [],
            isCentralAdmin: session.is_central_admin || false,
        });
    }

    get currentProgram() {
        return this.state.currentProgram;
    }

    get allowedPrograms() {
        return this.state.allowedPrograms;
    }

    get isMultiProgram() {
        return this.state.isCentralAdmin || this.state.allowedPrograms.length > 1;
    }

    async switchProgram(programId) {
        if (!programId || (this.state.currentProgram && this.state.currentProgram.id === programId)) {
            return;
        }
        await this.orm.call("res.users", "action_switch_program", [programId]);
        window.location.reload();
    }
}

export const systrayItem = {
    Component: ProgramMenu,
};

registry.category("systray").add("ProgramMenu", systrayItem, { sequence: 40 });
