import { Component, OnInit, Input, Optional, Inject } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormControl,
  Validators,
} from '@angular/forms';
import { UserService, UserResponse } from '../../services/user.service';
import { TeamService } from '../../services/team.service';
import {
  MatDialogRef,
  MAT_DIALOG_DATA,
  MatDialog,
} from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PlayerService } from '../../services/player.service';
import { SessionService } from '../../services/session.service';
import { TournamentService } from '../../services/tournament.service';
import { MatchService } from '../../services/match.service';
import { Router } from '@angular/router';
import { NavigationService } from '../../services/navigation.service';
import { Team } from '../../services/team.service';
import { DetailsContentComponent } from '../details-content/details-content.component';
import { PopupContentComponent } from '../popup-content/popup-content.component';
@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss'],
})
export class FormComponent implements OnInit {
  team: any = {};
  teamId: number = 0;
  player: any = {};
  tournament: any = {};
  match: any = {};
  fileName: string = '';
  display: FormControl = new FormControl('', Validators.required);
  @Input() matchId!: number;
  @Input() data: any;
  @Input() formType!:
    | 'user'
    | 'team'
    | 'player'
    | 'tournament'
    | 'match-update'
    | 'team-edit'
    | 'tournament-edit'
    | 'password'
    | 'player-edit';

  form: FormGroup;
  fields: any[] = [];
  user: UserResponse | null = null;
  userPassword: any = {};
  teams: Team[] = [];
  playerId: number | undefined;

  constructor(
    private formBuilder: FormBuilder,
    private userService: UserService,
    private dialog: MatDialog,
    @Optional() public dialogRef: MatDialogRef<FormComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public dialogData: any,
    private teamService: TeamService,
    private playerService: PlayerService,
    private snackBar: MatSnackBar,
    private sessionService: SessionService,
    private tournamentService: TournamentService,
    private matchService: MatchService,
    private router: Router,
    private navigationService: NavigationService,
  ) {
    this.form = this.formBuilder.group({ team_id: [null] });
    if (dialogData) {
      this.formType = dialogData.formType;
      this.data = dialogData.data;
      this.playerId = dialogData.playerId;
      this.fields = dialogData.fields;
    }
  }

  async ngOnInit(): Promise<void> {
    switch (this.formType) {
      case 'user':
        await this.initializeUserForm();
        break;
      case 'team':
        await this.initializeTeamForm();
        break;
      case 'player':
        await this.initializePlayerForm();
        await this.setTeamIdForPlayer();
        break;
      case 'tournament':
        await this.initializeTournamentForm();
        break;
      case 'match-update':
        await this.initializeMatchUpdateForm();
        break;
      case 'team-edit':
        await this.initializeTeamEditForm();
        break;
      case 'tournament-edit':
        await this.initializeTournamentEditForm();
        break;
      case 'password':
        await this.initializePasswordForm();
        break;
      case 'player-edit':
        await this.initializePlayerEditForm();
        break;
    }
  }

  async setTeamIdForPlayer(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (userId) {
      try {
        const user = await this.userService.getUser(Number(userId));
        if (user && user.team && user.team.id) {
          const teamId = user.team.id;
          this.form.patchValue({ team_id: teamId });
        } else {
          console.error('Team ID not found for user');
          this.snackBar.open('Team ID not found for user', 'Close', {
            duration: 2000,
          });
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.snackBar.open('Error fetching user data', 'Close', {
          duration: 2000,
        });
      }
    }
  }
  async initializeUserForm(): Promise<void> {
    const { user, fields } = await this.userService.getUserDataAndFields();
    this.user = user;
    this.fields = fields;
    this.initializeForm(this.fields);
  }

  async initializeTeamForm(): Promise<void> {
    this.fields = this.teamService
      .generateTeamFields(this.team)
      .filter((field) => ['name', 'logo'].includes(field.name));
    this.initializeForm(this.fields);
  }

  async initializeTeamEditForm(): Promise<void> {
    this.fields = this.teamService
      .generateTeamFields(this.team)
      .filter((field) => ['name'].includes(field.name));
    this.initializeForm(this.fields);
  }

  async initializeTournamentEditForm(): Promise<void> {
    this.teams = await this.teamService.getAllTeams();
    this.fields = this.tournamentService
      .generateTournamentEditFields(this.tournament, this.teams)
      .filter((field) =>
        ['name', 'amount_of_teams', 'date_of_tournament'].includes(field.name),
      );
    this.initializeForm(this.fields);
  }

  async initializePlayerForm(): Promise<void> {
    this.fields = this.playerService
      .generatePlayerFields(this.player)
      .filter((field) =>
        ['name', 'last_name', 'date_of_birth', 'gender'].includes(field.name),
      );
    this.initializeForm(this.fields);
    this.form.addControl('team_id', new FormControl(this.player.team_id || ''));
  }

  async initializePlayerEditForm(): Promise<void> {
    this.fields = this.playerService
      .generatePlayerFields(this.player)
      .filter((field) =>
        ['name', 'last_name', 'date_of_birth'].includes(field.name),
      );
    this.initializeForm(this.fields);
    this.form.addControl('team_id', new FormControl(this.player.team_id || ''));
  }

  async initializeTournamentForm(): Promise<void> {
    this.fields = this.tournamentService.generateTournamentFields(
      this.tournament,
    );
    this.initializeForm(this.fields);
    this.form.addControl('creator_id', new FormControl(''));
  }

  async initializeMatchUpdateForm(): Promise<void> {
    this.fields = this.matchService
      .generateMatchFields(this.match)
      .filter((field) => ['result'].includes(field.name));
    this.initializeForm(this.fields);
  }

  initializeForm(fields: any[]): void {
    const group: Record<string, any> = {};
    fields.forEach((field) => {
      group[field.name] = new FormControl(field.value || '');
    });
    this.form = new FormGroup(group);
  }

  async initializePasswordForm(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (!userId) {
      this.snackBar.open('User ID not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    const user = await this.userService.getUser(Number(userId));
    this.fields = await this.userService.generatePasswordFields(user);
    this.initializeForm(this.fields);
  }

  async submitForm(): Promise<void> {
    if (
      this.formType === 'team-edit' ||
      this.formType === 'user' ||
      this.formType === 'player-edit' ||
      this.formType === 'tournament-edit' ||
      this.formType === 'password'
    ) {
      const dialogRef = this.dialog.open(PopupContentComponent, {
        data: {
          dataType: 'edit-form',
        },
        height: '150px',
        width: '500px',
      });

      dialogRef.afterClosed().subscribe(async (confirmed: boolean) => {
        if (confirmed) {
          await this.handleFormSubmission();
        }
      });
    } else {
      await this.handleFormSubmission();
    }
  }

  private async handleFormSubmission(): Promise<void> {
    if (this.form.valid) {
      try {
        switch (this.formType) {
          case 'user':
            await this.submitUserForm();
            break;
          case 'team':
            await this.submitTeamForm();
            break;
          case 'player':
            await this.submitPlayerForm();
            break;
          case 'tournament':
            await this.submitTournamentForm();
            break;
          case 'team-edit':
            await this.submitTeamEditForm();
            break;
          case 'password':
            await this.submitPasswordForm();
            break;
          case 'player-edit':
            await this.submitPlayerEditForm();
            break;
          case 'tournament-edit':
            await this.submitTournamentEditForm();
            break;
        }
      } catch (error) {
        this.snackBar.open('Error submitting form', 'Close', {
          duration: 2000,
        });
      }
    }
  }

  async submitUserForm(): Promise<void> {
    if (this.user) {
      await this.userService.updateUser(this.user.id, this.form.value);
    }
    setTimeout(() => {
      this.navigationService.navigateToProfile().then(() => {
        window.location.reload();
      });
    }, 500);
  }

  async submitTeamForm(): Promise<void> {
    const teamName = this.form.value.name;
    const teamExists = await this.teamService.teamExists(teamName);
    const userId = this.sessionService.getUserId();
    const userHasTeam = await this.userService.userHasTeam(Number(userId));
    if (userHasTeam) {
      this.snackBar.open('You already have a team', 'Close', {
        duration: 5000,
      });
      return;
    }
    if (teamExists) {
      this.snackBar.open('Team already exists', 'Close', {
        duration: 2000,
      });
      return;
    }

    await this.teamService.createTeam(teamName);

    this.snackBar.open('Team created successfully', 'Close', {
      duration: 5000,
    });
    setTimeout(() => {
      this.navigationService.navigateToMyTeam().then(() => {
        window.location.reload();
      });
    }, 500);
  }

  async submitPlayerForm(): Promise<void> {
    const playerName = this.form.value.name;
    const playerLastName = this.form.value.last_name;
    const playerDOB = new Date(this.form.value.date_of_birth);

    const formattedDate = playerDOB.toISOString().split('T')[0];
    this.form.patchValue({ date_of_birth: formattedDate });

    const playerExists = await this.playerService.playerExists(
      playerName,
      playerLastName,
      formattedDate,
    );

    const teamId = this.form.value.team_id;

    const teamExists = await this.teamService.teamExistsById(teamId);

    if (!teamExists) {
      this.snackBar.open('Team not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    if (playerExists) {
      this.snackBar.open('Player already exists', 'Close', {
        duration: 2000,
      });
      return;
    }

    await this.playerService.createPlayer(this.form.value);
    this.snackBar.open('Player created successfully', 'Close', {
      duration: 5000,
    });
    setTimeout(() => {
      this.navigationService.navigateToMyTeam().then(() => {
        window.location.reload();
      });
    }, 500);
  }

  async submitPlayerEditForm(): Promise<void> {
    const playerName = this.form.value.name;
    const playerLastName = this.form.value.last_name;
    const playerDOB = new Date(this.form.value.date_of_birth);

    const formattedDate = playerDOB.toISOString().split('T')[0];
    this.form.patchValue({ date_of_birth: formattedDate });

    const playerExists = await this.playerService.playerExists(
      playerName,
      playerLastName,
      formattedDate,
    );

    const teamId = this.form.value.team_id;

    const teamExists = await this.teamService.teamExistsById(teamId);

    if (!teamExists) {
      this.snackBar.open('Team not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    if (playerExists) {
      this.snackBar.open('Player already exists', 'Close', {
        duration: 2000,
      });
      return;
    }

    if (this.playerId) {
      await this.playerService.updatePlayer(this.playerId, this.form.value);
      this.snackBar.open('Player Updated successfully', 'Close', {
        duration: 5000,
      });
      setTimeout(() => {
        this.navigationService.navigateToMyTeam().then(() => {
          window.location.reload();
        });
      }, 500);
    } else {
      console.error('Player ID is undefined');
    }
  }

  async submitTournamentForm(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (!userId) {
      this.snackBar.open('User ID not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    this.form.patchValue({ creator_id: Number(userId) });

    const tournamentName = this.form.value.name;
    const tournamentExists =
      await this.tournamentService.tournamentExists(tournamentName);
    if (tournamentExists) {
      this.snackBar.open('Tournament already exists', 'Close', {
        duration: 2000,
      });
      return;
    }

    const activeTournaments = await this.userService.getUserActiveTournament(
      Number(userId),
    );
    if (activeTournaments.length > 0) {
      this.snackBar.open('You have already active tournament', 'Close', {
        duration: 5000,
      });
      return;
    }

    const tournamentDate = new Date(this.form.value.date_of_tournament);
    const today = new Date();
    const sixMonthsFromNow = new Date();
    sixMonthsFromNow.setMonth(today.getMonth() + 6);

    if (tournamentDate < today || tournamentDate > sixMonthsFromNow) {
      this.snackBar.open(
        'Tournament date must be within the next 6 months',
        'Close',
        {
          duration: 5000,
        },
      );
      return;
    }

    const formattedDate = tournamentDate.toISOString().split('T')[0];
    this.form.patchValue({ date_of_tournament: formattedDate });

    if (!this.form.value.creator_id) {
      console.error('creator_id is not set in the form');
      return;
    }

    try {
      await this.tournamentService.createTournament(this.form.value);
      this.snackBar.open('Tournament created successfully', 'Close', {
        duration: 5000,
      });

      //Reload
      setTimeout(() => {
        this.router.navigateByUrl('/tournament-base').then(() => {
          window.location.reload();
        });
      }, 500);
    } catch (error) {
      console.error('Error submitting form:', error);
      this.snackBar.open('Error submitting form', 'Close', {
        duration: 5000,
      });
    }
  }

  async submitTournamentEditForm(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (!userId) {
      this.snackBar.open('User ID not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    this.form.patchValue({ creator_id: Number(userId) });

    const tournamentName = this.form.value.name;
    const tournamentExists =
      await this.tournamentService.tournamentExists(tournamentName);
    if (tournamentExists) {
      this.snackBar.open('Tournament already exists', 'Close', {
        duration: 2000,
      });
      return;
    }

    const activeTournaments = await this.userService.getUserActiveTournament(
      Number(userId),
    );

    if (activeTournaments.length === 0) {
      this.snackBar.open('No active tournament found', 'Close', {
        duration: 5000,
      });
      return;
    }

    const activeTournamentId = activeTournaments[0].id;

    const tournamentDate = new Date(this.form.value.date_of_tournament);
    const today = new Date();
    const sixMonthsFromNow = new Date();
    sixMonthsFromNow.setMonth(today.getMonth() + 6);

    if (tournamentDate < today || tournamentDate > sixMonthsFromNow) {
      this.snackBar.open(
        'Tournament date must be within the next 6 months',
        'Close',
        {
          duration: 5000,
        },
      );
      return;
    }

    const formattedDate = tournamentDate.toISOString().split('T')[0];
    this.form.patchValue({ date_of_tournament: formattedDate });

    try {
      await this.tournamentService.updateTournament(
        activeTournamentId,
        this.form.value,
      );
      this.snackBar.open('Tournament updated successfully', 'Close', {
        duration: 5000,
      });

      setTimeout(() => {
        this.navigationService.navigateToMyTournament().then(() => {
          window.location.reload();
        });
      }, 500);
    } catch (error) {
      console.error('Error submitting form:', error);
      this.snackBar.open('Error submitting form', 'Close', {
        duration: 5000,
      });
    }
  }

  async submitTeamEditForm(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (userId) {
      const userTeam = await this.userService.getUserTeam(Number(userId));
      this.teamId = userTeam.id;
    }

    const data = {
      name: this.form.value.name,
      league_id: this.form.value.league_id,
    };

    try {
      await this.teamService.updateTeam(this.teamId, data);
      this.snackBar.open('Team updated successfully', 'Close', {
        duration: 5000,
      });
      setTimeout(() => {
        this.navigationService.navigateToMyTeam().then(() => {
          window.location.reload();
        });
      }, 500);
    } catch (error) {
      console.error('Error updating team:', error);
      this.snackBar.open('Error updating team', 'Close', {
        duration: 2000,
      });
    }
  }

  async submitPasswordForm(): Promise<void> {
    const userId = this.sessionService.getUserId();
    if (!userId) {
      this.snackBar.open('User ID not found', 'Close', {
        duration: 2000,
      });
      return;
    }

    const { password, new_password, confirm_new_password } = this.form.value;

    if (new_password !== confirm_new_password) {
      this.snackBar.open(
        'New password and confirm password do not match',
        'Close',
        {
          duration: 2000,
        },
      );
      return;
    }

    try {
      await this.userService.changePassword(Number(userId), {
        password,
        new_password,
        confirm_new_password,
      });
      this.snackBar.open('Password changed successfully', 'Close', {
        duration: 5000,
      });
      this.dialogRef.close();
    } catch (error) {
      console.error('Error changing password:', error);
      this.snackBar.open('Error changing password', 'Close', {
        duration: 5000,
      });
    }
  }

  cancel(): void {
    this.dialogRef.close();
  }

  trackByFn(index: number, item: any): any {
    return item.name;
  }
}
