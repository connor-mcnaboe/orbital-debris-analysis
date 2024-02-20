import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup} from "@angular/forms";
import {MissionService} from "../services/mission.service";
import {MissionDataShareService, ThreatReport} from "../services/mission-data-share.service";

@Component({
  selector: 'app-mission',
  templateUrl: './mission.component.html',
  styleUrls: ['./mission.component.scss']
})
export class MissionComponent implements OnInit {
  missionForm: FormGroup;

  constructor(private missionService: MissionService,
              private formBuilder: FormBuilder,
              private missionDataShare: MissionDataShareService) { }

  ngOnInit(): void {
    this.buildForm();
  }

  buildForm(): void {
    this.missionForm = this.formBuilder.group({
      apogee: 0,
      perigee: 0,
      threat_tolerance_km: 0,
    });
  }

  submitMission(): void {
    this.missionService.postMissionDto(this.missionForm.value)
      .subscribe((threatReport: ThreatReport)=> {
        this.missionDataShare.update_mission(threatReport)
      })
  }
}
